URL=http://127.0.0.1:5000

QUESTION="What do you know about Drax power plant?"

DATA='{
     "question": "'${QUESTION}'"
}'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${DATA}" \
  ${URL}/question 


