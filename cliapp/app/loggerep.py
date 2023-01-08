from logging.config import dictConfig

from fastapi import FastAPI
from pydantic import BaseModel
import logging

EDR = 5
logging.addLevelName(EDR, 'main')

def edr(self, message, *args, **kws):
    self.log(EDR, message, *args, **kws)
logging.Logger.edr = edr

logger = logging.getLogger('main')

class LogItem(BaseModel):
    content: str

app = FastAPI()

@app.post("/edr/log")
def write__edr_log(log: LogItem):
    logger.edr(log.content)