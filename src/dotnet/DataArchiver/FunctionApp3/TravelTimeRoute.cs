using System;

namespace WSDOT
{
    public class TravelTimeRoute
    {
        public int TravelTimeID { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public DateTime TimeUpdated { get; set; }
        public object StartPoint { get; set; }
        public object EndPoint { get; set; }
        public float Distance { get; set; }
        public int AverageTime { get; set; }
        public int CurrentTime { get; set; }
    }
}
