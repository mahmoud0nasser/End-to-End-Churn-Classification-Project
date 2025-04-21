from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from utils.inference import predict_new
from utils.config import APP_NAME, VERSION, SECRET_KEY_TOKEN, preprocessor, forest_model, xgboost_model
from utils.request import CustomerData

# Initialize an app
app = FastAPI(title=APP_NAME, version=VERSION)
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_methods=["*"],
   allow_headers=["*"],
)

api_key_header = APIKeyHeader(name='X-API-Key')
async def verify_api_key(api_key: str=Depends(api_key_header)):
    if api_key != SECRET_KEY_TOKEN:
        raise HTTPException(status_code=403, detail="You are not authorized to use this API")
    return api_key

@app.get('/', tags=['General'], description="General Check Of API")
async def home(api_key: str=Depends(verify_api_key)) -> dict:
    return {
        "mesage": f"Welcome to {APP_NAME}",
        "version": f"{VERSION}",
        "status": "UP & Running"
    }

@app.post('/predict/forest', tags=['Models'], description="Prediction of Churn Using RandomForest")
async def predict_forest(data: CustomerData, api_key: str=Depends(verify_api_key)) -> dict:
    try:
        # Call the Function
        response = predict_new(data=data, pipeline=preprocessor, model=forest_model)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"There is a problem in prediction using RandomForest, {str(e)}")
    

@app.post("/predict/xgboost", tags=['Models'], description="Prediction of Churn Using XGBoost") 
async def predict_xgboost(data: CustomerData, api_key: str=Depends(verify_api_key)) -> dict:
   
   try:
       response = predict_new(data=data, pipeline=preprocessor, model=xgboost_model)
       return response
   
   except Exception as e:
       raise HTTPException(status_code=500, detail=f"There is a problem in prediction using XGBoost, {str(e)}")

# Run Via Terminal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, reload=True)
