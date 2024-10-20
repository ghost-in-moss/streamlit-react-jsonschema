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
    age: int = Field(2, description="bar value")
    some_float: float = Field(description="test about float value")

    students: List[Student] = Field(default_factory=list, description="list of students")
    students_dict: Dict[str, Student] = Field(default_factory=dict, description="dict of students")


count = 0
if "count" not in st.session_state:
    st.session_state["count"] = count
else:
    count = st.session_state["count"]


st.title("Streamlit-react-jsonschema Example" + str(count))
with st.expander("source code of the example pydantic class", expanded=True):
    codes = inspect.getsource(SomeClass)
    st.code(codes)

data = None
if "data" in st.session_state:
    data = st.session_state["data"]

st.write(data)
st.divider()
value, submitted = srj.pydantic_form(model=SomeClass, readonly=count > 3, data=data)
if submitted:
    data = value.model_dump()
    st.session_state["data"] = data
    st.write("saving data to session")

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
