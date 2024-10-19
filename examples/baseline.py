from typing import Union, List, Dict
import streamlit as st
import streamlit_react_jsonschema as srj
import inspect
from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str = Field(description="name of the student")
    level: int = Field(description="level of the student")


class SomeClass(BaseModel):
    """
    test class of pydantic model Foo
    """
    name: Union[str, None] = Field(None, description="filed with optional[str]")
    age: int = Field(0, description="bar value")
    some_float: float = Field(description="test about float value")

    students: List[Student] = Field(default_factory=list, description="list of students")
    students_dict: Dict[str, Student] = Field(default_factory=dict, description="dict of students")


st.title("Streamlit-react-jsonschema Example")
with st.expander("source code of the example pydantic class", expanded=True):
    codes = inspect.getsource(SomeClass)
    st.code(codes)

count = 0
if "count" not in st.session_state:
    st.session_state["count"] = count
else:
    count = st.session_state["count"]
value, submitted = srj.pydantic_form(model=SomeClass, disabled=count > 0)

st.subheader("result:")
st.write(f"submitted: {submitted}")
st.write(f"type of the result: {type(value)}")
st.write(value)
if isinstance(value, BaseModel):
    st.write("model dump value")
    st.write(value.model_dump(exclude_defaults=False))

if rerun := st.button("rerun"):
    st.session_state["count"] = count + 1
    st.write(f"rerun: {count}")
