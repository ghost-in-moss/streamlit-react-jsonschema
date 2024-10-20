from typing import Union, List, Dict
import streamlit as st
import streamlit_react_jsonschema as srj
import inspect
from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str = Field(description="name of the student")
    level: int = Field(description="level of the student")


value, submitted = srj.pydantic_form(model=Student, disabled=True)

st.subheader("result:")
st.write(f"submitted: {submitted}")
st.write(f"type of the result: {type(value)}")
st.write(value)


value, submitted = srj.pydantic_form(model=Student, disabled=True, data={"name": "foo"}, key="abc")

st.subheader("result:")
st.write(f"submitted: {submitted}")
st.write(f"type of the result: {type(value)}")
st.write(value)
