using System.Collections.Concurrent;
using UnityEngine;
using OscJack;

public class CustomOSCReceiver : MonoBehaviour
{
    public string oscAddress = "/franui/object/3/rotation/z";
    public OscConnection connection;
    public CasitaEvents casitaEvents;  // Reference to your CasitaEvents script

    public int EventIndex = 0;

    private ConcurrentQueue<int> intQueue = new ConcurrentQueue<int>();
    private ConcurrentQueue<float> floatQueue = new ConcurrentQueue<float>();

    private float previousX = 0f;
    private float previousY = 0f;
    private float previousZ = 0f;
    private float alpha = 0.5f; // Smoothing factor

    void Start()
    {
        var server = OscMaster.GetSharedServer(connection.port);
        server.MessageDispatcher.AddCallback(oscAddress, OnDataReceive);
    }

    void OnDataReceive(string address, OscDataHandle data)
    {
        if (EventIndex == 1 || EventIndex == 2 || EventIndex == 7|| EventIndex == 8|| EventIndex == 9|| EventIndex == 10)
        {
            int payload = data.GetElementAsInt(0);
            intQueue.Enqueue(payload);
            Debug.Log($"Received OSC message at {address} with value: {payload}");

        }
        else
        {
            float payload = data.GetElementAsFloat(0);
            floatQueue.Enqueue(payload);
            Debug.Log($"Received OSC message at {address} with value: {payload}");
        }
    }

    void Update()
    {
        while (intQueue.TryDequeue(out int payload))
        {
            if (EventIndex == 1)
                casitaEvents.CasitaEntersEvent(payload);
            else if (EventIndex == 2)
                casitaEvents.CasitaLeavesEvent(payload);

            else if (EventIndex == 7){
                Debug.Log("event index 7, pagina 1");
                casitaEvents.PageEntersEvent(1);
            }
            else if (EventIndex == 8){
                Debug.Log("event index 8, pagina 2");
                casitaEvents.PageEntersEvent(2);
            }
            else if (EventIndex == 9){
                Debug.Log("event index 9, pagina 3");
                casitaEvents.PageEntersEvent(3);
            }
            else if (EventIndex == 10){
                Debug.Log("event index 10, pagina 4");
                casitaEvents.PageEntersEvent(4);
            }
        }

        while (floatQueue.TryDequeue(out float payload))
        {
            if (EventIndex == 3)
            {
                float smoothedX = alpha * payload + (1 - alpha) * previousX;
                previousX = smoothedX;
                casitaEvents.CasitaUpdatePositionXEvent(smoothedX);
            }
            else if (EventIndex == 4)
            {
                float smoothedY = alpha * payload + (1 - alpha) * previousY;
                previousY = smoothedY;
                casitaEvents.CasitaUpdatePositionYEvent(smoothedY);
            }
            else if (EventIndex == 5)
            {
                float smoothedZ = alpha * payload + (1 - alpha) * previousZ;
                previousZ = smoothedZ;
                casitaEvents.CasitaUpdateRotationZEvent(smoothedZ);
            }
        }
    }
}
