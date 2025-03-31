from fastapi import FastAPI
from device_reader import AD4USBReader

app = FastAPI()
reader = AD4USBReader(port="COM3")  # Change COM port if needed

@app.get("/input1")
def get_input1():
    value = reader.read_input(1)
    return {"input1": value}

@app.get("/input2")
def get_input2():
    value = reader.read_input(2)
    return {"input2": value}
