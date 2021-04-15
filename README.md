### Instructions

- Clone the repository
- Install all the mentioned dependencies in requirements.txt 
- Start the redis server on port 6379
- Run the django server on port 8000

### API's

##### Get Records 
HTTP METHOD: GET
URL: http://localhost:8000/api/core/get-records/
PARAMS: { date: date, q: searchQuery }
RESPONSE: List of records

##### Download CSV 
HTTP METHOD: GET
URL: http://localhost:8000/api/core/get-records/
PARAMS: { date: date, q: searchQuery }
RESPONSE: CSV FIle


### Vue.js Client

`<VueJS  Client Repo Link>` : <https://github.com/satyachaurasia/Zerodha-Frontend>
