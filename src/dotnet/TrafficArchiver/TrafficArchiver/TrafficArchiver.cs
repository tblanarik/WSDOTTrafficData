using System;
using System.Net;
using Microsoft.Azure.WebJobs;
using System.IO;
using System.Collections.Generic;
using Newtonsoft.Json;
using Microsoft.Azure.EventHubs;
using System.Text;
using Microsoft.Extensions.Logging;

namespace TrafficArchiver
{
    public static class TrafficArchiver
    {
        [FunctionName("TrafficArchiver")]
        public static void Run([TimerTrigger("0 */20 * * * *")]TimerInfo myTimer, ILogger log)
        {
            log.LogInformation(JsonConvert.SerializeObject(new
            {
                Event = "TrafficArchiverStarted"
            }));
            var status = "Success";
            try
            {
            var hubName = Environment.GetEnvironmentVariable("EventHubName");
            var url = Environment.GetEnvironmentVariable("TravelTimeUrl");
            var connectionString = Environment.GetEnvironmentVariable("EventHubConnectionString");

            var routes = MakeWSDOTHttpRequest(url, log);
            var routeStrings = routes.ConvertAll(x => x.GetJson());
            string recordString = string.Join(Environment.NewLine, routeStrings);

            EventData eventData = new EventData(Encoding.UTF8.GetBytes(recordString));
            var eventHubClient = EventHubClient.CreateFromConnectionString(connectionString);
            eventHubClient.SendAsync(eventData);
            }
            catch (Exception _e)
            {
                status = "Failed";
                log.LogError(_e,
                             JsonConvert.SerializeObject(new
                             {
                                 Event = "TrafficArchiverError"
                             })
                    );
            }
            log.LogInformation(JsonConvert.SerializeObject(new
            {
                Event = "TrafficArchiverCompleted",
                Status = status
            }));
        }

        public static List<TravelTimeRoute> MakeWSDOTHttpRequest(string wsdotUrl, ILogger log)
        {
            log.LogInformation(JsonConvert.SerializeObject(new
            {
                Event = "BeginWsdotRequest"
            }));

            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(wsdotUrl);
            request.Method = "GET";
            request.ContentType = "application/json";
            var resp = request.GetResponse();
            var dataStream = resp.GetResponseStream();
            var reader = new StreamReader(dataStream);
            string responseFromServer = reader.ReadToEnd();
            reader.Close();
            resp.Close();
            var response = JsonConvert.DeserializeObject<List<TravelTimeRoute>>(responseFromServer);
            log.LogInformation(JsonConvert.SerializeObject(new
            {
                Event = "EndWsdotRequest",
                ResponseLength = response.Count
            }));
            return response;
        }
    }
}
