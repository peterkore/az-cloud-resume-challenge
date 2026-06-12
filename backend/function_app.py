import azure.functions as func
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="GetResumeCounter")
@app.cosmos_db_input(arg_name="inputDocument", 
                     database_name="AzureResume", 
                     container_name="CounterContainer",
                     id="1",
                     partition_key="1",
                     connection="AzureCosmosDBConnectionString")
@app.cosmos_db_output(arg_name="outputDocument", 
                      database_name="AzureResume", 
                      container_name="CounterContainer",
                      connection="AzureCosmosDBConnectionString")
def GetResumeCounter(req: func.HttpRequest, 
                     inputDocument: func.DocumentList, 
                     outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    # Ha a dokumentum nem létezik (biztonsági játék), létrehozzuk az alapot
    if not inputDocument:
        counter = {"id": "1", "count": 1}
    else:
        # Kivesszük az első (és egyetlen) dokumentumot a listából
        counter = inputDocument[0]
        # Megnöveljük a látogatottság számát eggyel
        counter['count'] += 1

    # Az output binding segítségével visszamentjük a frissített JSON-t a Cosmos DB-be
    outputDocument.set(func.Document.from_dict(counter))

    # Visszaküldjük a frontendnek az új értéket JSON formátumban, CORS-fejléccel
    return func.HttpResponse(
        body=json.dumps({"count": counter['count']}),
        status_code=200,
        mimetype="application/json",
        headers={
            "Access-Control-Allow-Origin": "*", # CORS engedélyezése, hogy a weboldalad meg tudja hívni
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )