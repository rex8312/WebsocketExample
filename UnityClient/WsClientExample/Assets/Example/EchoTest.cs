using UnityEngine;
using System.Collections;
using System;
using LitJson;


public class Message
{
	public string msg { get; set; }
	public int no { get; set; }
}


public class EchoTest : MonoBehaviour {

	// Use this for initialization
	IEnumerator Start () {
		WebSocket w = new WebSocket(new Uri("ws://127.0.0.1:8080/websocket"));
		yield return StartCoroutine(w.Connect());

		int i = 0;
		w.SendString(PackMessage("Hi there", i));
		while (true)
		{
			string reply = w.RecvString();
			if (reply != null)
			{
				Message msg = UnpackMessage (reply);
				Debug.Log ("Received: " + msg.msg + ", " + msg.no);
				w.SendString (PackMessage ("Hi there", i));
			}
			if (w.error != null)
			{
				Debug.LogError ("Error: " + w.error);
				break;
			}

			++i;

			yield return 0;
		}
		w.Close();
	}

	private string PackMessage(string m, int n)
	{
		Message msg = new Message ();
		msg.msg = m;
		msg.no = n;
		return JsonMapper.ToJson(msg);
	}

	private Message UnpackMessage(string resp)
	{
		return LitJson.JsonMapper.ToObject <Message> (resp);
	}
}
