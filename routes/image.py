from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import httpx

router = APIRouter()

@router.get("/fetch-image", response_class=Response)
async def fetch_image():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("192.168.1.103/5000/capture")
            response.raise_for_status()
            # Return raw JPEG bytes with correct mimetype
            return Response(content=response.content, media_type="image/jpeg")
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Camera API unavailable")