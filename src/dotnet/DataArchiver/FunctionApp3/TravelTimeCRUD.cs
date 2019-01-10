using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data.SqlClient;
using System.IO;
using System.Net;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Newtonsoft.Json;

namespace WSDOT
{
    public static class TravelTimeCRUD
    {
        [FunctionName("TravelTimeCRUD")]
        public static void Run([TimerTrigger("0 */20 * * * *")]TimerInfo myTimer, TraceWriter log)
        {
            GetTravelTimes(log);
        }

        public static void GetTravelTimes(TraceWriter log)
        {
            log.Info("Making WSDOT Request");
            var ttRoutes = RetrieveWSDOTData(log);
            log.Info("Completed WSDOT Request");
            
            log.Info("Starting DB Insert");
            InsertRow(ttRoutes, log);
            log.Info("Finished DB Insert");
        }

        public static List<TravelTimeRoute> RetrieveWSDOTData(TraceWriter log)
        {
            var wsdotUrl = ConfigurationManager.AppSettings["WSDOTUrl"];
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(wsdotUrl);
            request.Method = "GET";
            request.ContentType = "application/json";
            var resp = request.GetResponse();
            var dataStream = resp.GetResponseStream();
            var reader = new StreamReader(dataStream);
            string responseFromServer = reader.ReadToEnd();
            var ttRoutes = JsonConvert.DeserializeObject<List<TravelTimeRoute>>(responseFromServer); 
            reader.Close();
            resp.Close();

            return ttRoutes;
        }

        public static void InsertRow(List<TravelTimeRoute> ttRoutes, TraceWriter log)
        {
            //INSERT INTO TravelTimes VALUES(value1, value2, value3, ...);

            var connectionString = ConfigurationManager.AppSettings["DBConnString"];
            
            using (SqlConnection connection = new SqlConnection(connectionString))
            {
                connection.Open();
                var state = connection.State;
                foreach(var route in ttRoutes)
                {
                    try
                    {
                        var commandStr = $"INSERT INTO TravelTimes VALUES({route.TravelTimeID}, '{route.Name}', '{route.Description}', '{route.TimeUpdated}', {route.Distance}, {route.AverageTime}, {route.CurrentTime});";
                        using (SqlCommand command = new SqlCommand(commandStr, connection))
                        {
                            command.ExecuteNonQuery();
                        }
                        log.Info($"Row inserted: {route.TravelTimeID} for time {route.TimeUpdated}");
                    }
                    catch (Exception ex)
                    {
                        log.Warning($"Failed to insert {route.TravelTimeID} for time {route.TimeUpdated} because: {ex.Message}");
                    }
                }
            }
        }

        public static void CreateTable()
        {
            var connectionString = ConfigurationManager.AppSettings["DBConnString"];

            using (SqlConnection connection =
            new SqlConnection(connectionString))
            {
                var commandStr = "If not exists (select name from sysobjects where name = 'TravelTimes') CREATE TABLE TravelTimes(TravelTimeID INT,Name CHAR(255),Description TEXT,TimeUpdated DATETIME, Distance FLOAT, AverageTime INT, CurrentTime INT)";

                using (SqlCommand command = new SqlCommand(commandStr, connection))
                {
                    command.ExecuteNonQuery();
                }
            }
        }

    }
}
