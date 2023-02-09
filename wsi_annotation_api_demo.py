import requests
import json

url = 'https://9mtn9h99o3.execute-api.us-east-2.amazonaws.com/default/wsi-frame-split'
data = {
    'dicom_path': [
        "01cd892e-5dbc-4792-ace6-d03a9b363b7c",
        "036ccb2a-36a9-411d-82f6-8ee58c1ed56c",
        "228c7c4b-9f15-4f3e-bb13-900cdebb495b",
        "27b58e8b-658c-434c-bdaa-5c782c529d9c",
        "41c132a6-be90-4feb-9630-c21164539e66",
        "5184f031-e05e-4c25-98e6-21c5f91dcbfb",
        "5dfb91d1-6000-460a-bdd5-6af5ee92178e",
        "752ee69c-518b-4e93-9a06-0d5cc91c6b45",
        "7e27d6cf-3e03-4486-b758-a4418407d5fd",
        "85584502-4590-4383-a0fc-09c18829beed",
        "b1cedd2f-48ea-4830-895e-82b932856272",
        "b482dabf-6efa-45b4-9d72-2170bee7a618",
        "b7eb7a66-aff2-4261-98d2-ac981408b4d7",
        "bd02acb6-f5aa-449c-90ac-29b9fc06b055",
        "c03e2213-d669-4147-b658-4578e75cb9e7",
        "d873f68d-aace-4e4f-a730-b848fd471b58",
        "dc945bc6-5937-4331-b340-59f94fc2a78b",
        "e0f678e2-04f7-43be-832a-9fbd1e99f3f9",
        "e158199a-25ac-4a28-a12d-bbbcb65fcc09",
        "f9037d81-e51a-4ff7-9e88-e2420cebcf9b"
    ],
    'annotation_path': [
        "104a24bf-3a9b086a-667adeb1-703db9ad"
    ],
    'sampleid': 'hello'
}

headers = {'x-api-key': 'AsiUqAkPtGa8TaAFwNTTS2RrLHbxB6BQ5fM7HdEw'}

print(requests.post(url, headers=headers, data=json.dumps(data)))
