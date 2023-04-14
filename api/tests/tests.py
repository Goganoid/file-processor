from chalice.test import Client
import json
from app import app


def test_index_valid_url():
     with Client(app) as client:
         response = client.http.post(
           '/',
           headers={'Content-Type':'application/json'},
           body=json.dumps({'fileUrl':'https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg'})
       )
         assert response.status_code == 200

def test_index_no_url():
     with Client(app) as client:
         response = client.http.post(
           '/',
           headers={'Content-Type':'application/json'},
           body=json.dumps({})
       )
         assert response.status_code == 400

def test_index_empty_url():
     with Client(app) as client:
         response = client.http.post(
           '/',
           headers={'Content-Type':'application/json'},
           body=json.dumps({'fileUrl':''})
       )
         assert response.status_code == 400

def test_index_wrong_type():
     with Client(app) as client:
         response = client.http.post(
           '/',
           headers={'Content-Type':'application/json'},
           body=json.dumps({'fileUrl':'https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.txt'})
       )
         assert response.status_code == 400