using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class CasitaEvents : MonoBehaviour
{

    [Header("Calibration Settings")]
    public float minXValue = -0.5f;  // Default min value
    public float maxXValue = 0.5f;   // Default max value

    public float minYValue = 0.5f;  // Default min value
    public float maxYValue = -0.5f;   // Default max value

    public int pageNum = 0; // Default starting page

    // The plane object
    public GameObject plane;
    public GameObject modelo3D;

    public GameObject faroPagina1;
    public GameObject faroPagina2;
    public GameObject faroPagina3;
    public GameObject faroPagina4;

    public GameObject molinoPagina1;
    public GameObject molinoPagina2;
    public GameObject molinoPagina3;
    public GameObject molinoPagina4;

    public GameObject puertaPagina1;
    public GameObject puertaPagina2;
    public GameObject puertaPagina3;
    public GameObject puertaPagina4;

    public GameObject pozoPagina1;
    public GameObject pozoPagina2;
    public GameObject pozoPagina3;
    public GameObject pozoPagina4;


    // Start is called before the first frame update
    void Start()
    {
        if (plane == null)
        {
            plane = transform.parent.gameObject; // Assume parent is the plane if not set
        }
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void CasitaEntersEvent(int check) // Event 1
    {
        // Activate Mesh Renderer from this object
        modelo3D.SetActive(true);
    }

    public void CasitaLeavesEvent(int check) // Event 2
    {
        // Deactivate Mesh Renderer from this object
        modelo3D.SetActive(false);
    }

    public void CasitaUpdatePositionXEvent(float pos) // Event 3
    {
        if (plane != null)
        {
            // Get the bounds of the plane
            Renderer planeRenderer = plane.GetComponent<Renderer>();
            float planeWidth = planeRenderer.bounds.size.x;
            float planeLeftExtreme = planeRenderer.bounds.min.x;
            float planeRightExtreme = planeRenderer.bounds.max.x;

            // Map the received value to the plane's X bounds
            float mappedX = Mathf.Lerp(planeLeftExtreme, planeRightExtreme, Mathf.InverseLerp(minXValue, maxXValue, pos));

            // Update the object's position
            Vector3 newPosition = transform.localPosition;
            newPosition.x = mappedX;
            transform.localPosition = newPosition;
        }
        else
        {
            Debug.LogError("Plane object is not set or found.");
        }
    }

    public void CasitaUpdatePositionYEvent(float pos) // Event 4
    {
        if (plane != null)
        {
            // Get the bounds of the plane
            Renderer planeRenderer = plane.GetComponent<Renderer>();
            float planeWidth = planeRenderer.bounds.size.z;
            float planeLeftExtreme = planeRenderer.bounds.min.z;
            float planeRightExtreme = planeRenderer.bounds.max.z;

            // Map the received value to the plane's X bounds
            float mappedZ = Mathf.Lerp(planeLeftExtreme, planeRightExtreme, Mathf.InverseLerp(minYValue, maxYValue, pos));

            // Update the object's position
            Vector3 newPosition = transform.localPosition;
            newPosition.z = mappedZ;
            transform.localPosition = newPosition;
        }
        else
        {
            Debug.LogError("Plane object is not set or found.");
        }
    }

    public void CasitaUpdateRotationZEvent(float rot) // Event 5
    {
        // Rotate the object in Y axis (rot will came from 0 to 180 and -180 to 0)
        this.transform.rotation = Quaternion.Euler(0, rot, 0);
    }

    public void PageEntersEvent(int pageNum)
    {
        Debug.Log("Page enters event: " + pageNum);
        this.pageNum = pageNum;

        if (this.pageNum == 1)
        {
            this.faroPagina1.SetActive(true);
            this.faroPagina2.SetActive(false);
            this.faroPagina3.SetActive(false);
            this.faroPagina4.SetActive(false);
            this.molinoPagina1.SetActive(true);
            this.molinoPagina2.SetActive(false);
            this.molinoPagina3.SetActive(false);
            this.molinoPagina4.SetActive(false);
            this.puertaPagina1.SetActive(true);
            this.puertaPagina2.SetActive(false);
            this.puertaPagina3.SetActive(false);
            this.puertaPagina4.SetActive(false);
            this.pozoPagina1.SetActive(true);
            this.pozoPagina2.SetActive(false);
            this.pozoPagina3.SetActive(false);
            this.pozoPagina4.SetActive(false);
        }
        else if (this.pageNum == 2)
        {
            this.faroPagina1.SetActive(false);
            this.faroPagina2.SetActive(true);
            this.faroPagina3.SetActive(false);
            this.faroPagina4.SetActive(false);
            this.molinoPagina1.SetActive(false);
            this.molinoPagina2.SetActive(true);
            this.molinoPagina3.SetActive(false);
            this.molinoPagina4.SetActive(false);
            this.puertaPagina1.SetActive(false);
            this.puertaPagina2.SetActive(true);
            this.puertaPagina3.SetActive(false);
            this.puertaPagina4.SetActive(false);
            this.pozoPagina1.SetActive(false);
            this.pozoPagina2.SetActive(true);
            this.pozoPagina3.SetActive(false);
            this.pozoPagina4.SetActive(false);
        }
        else if (this.pageNum == 3)
        {
            this.faroPagina1.SetActive(false);
            this.faroPagina2.SetActive(false);
            this.faroPagina3.SetActive(true);
            this.faroPagina4.SetActive(false);
            this.molinoPagina1.SetActive(false);
            this.molinoPagina2.SetActive(false);
            this.molinoPagina3.SetActive(true);
            this.molinoPagina4.SetActive(false);
            this.puertaPagina1.SetActive(false);
            this.puertaPagina2.SetActive(false);
            this.puertaPagina3.SetActive(true);
            this.puertaPagina4.SetActive(false);
            this.pozoPagina1.SetActive(false);
            this.pozoPagina2.SetActive(false);
            this.pozoPagina3.SetActive(true);
            this.pozoPagina4.SetActive(false);
        }
        else if (this.pageNum == 4)
        {
            this.faroPagina1.SetActive(false);
            this.faroPagina2.SetActive(false);
            this.faroPagina3.SetActive(false);
            this.faroPagina4.SetActive(true);
            this.molinoPagina1.SetActive(false);
            this.molinoPagina2.SetActive(false);
            this.molinoPagina3.SetActive(false);
            this.molinoPagina4.SetActive(true);
            this.puertaPagina1.SetActive(false);
            this.puertaPagina2.SetActive(false);
            this.puertaPagina3.SetActive(false);
            this.puertaPagina4.SetActive(true);
            this.pozoPagina1.SetActive(false);
            this.pozoPagina2.SetActive(false);
            this.pozoPagina3.SetActive(false);
            this.pozoPagina4.SetActive(true);
        }
    }
}
