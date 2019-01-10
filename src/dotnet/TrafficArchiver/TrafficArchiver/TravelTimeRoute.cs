using System;
using Newtonsoft.Json;

namespace TrafficArchiver
{
    public class TravelTimeRoute
    {
        public int TravelTimeID { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public DateTime TimeUpdated { get; set; }
        public double Distance { get; set; }
        public int AverageTime { get; set; }
        public int CurrentTime { get; set; }

        public string Repr()
        {
            return $"TravelTimeRoute: {TravelTimeID} - {TimeUpdated}";
        }

        public string GetJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}