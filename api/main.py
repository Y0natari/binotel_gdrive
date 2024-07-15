from fastapi import FastAPI, Request
import logging
import asyncio

from utils import fetch_call_record, download_to_buffer, upload_to_google_drive, generate_filename

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.post("/")
async def api_call_completed(request: Request):
    form = await request.form()
    data = dict(form)
    
    try:
        call_details = {key: value for key, value in data.items() if key.startswith("callDetails")}
        general_call_id = call_details.get("callDetails[generalCallID]")
        if general_call_id:
            await asyncio.sleep(120) # Sleep for some time until Binotel uploads the file to Amazon servers
            call_url = await fetch_call_record(general_call_id)
            if call_url:
                file_buffer = await download_to_buffer(call_url)
                file_name = generate_filename()
                upload_to_google_drive(file_buffer, file_name)
    except Exception as e:
        logging.error(f"Error processing request: {e}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=444)
