import os
import streamlit as st
import streamlit.components.v1 as components
from typing import Type, Dict, Optional, Tuple
from pydantic import BaseModel

__all__ = [
    'jsonschema_form',
    'pydantic_form',
    'pydantic_instance_form',
]

_RELEASE = True

COMPONENT_NAME = "streamlit_react_jsonschema"

if not _RELEASE:
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(COMPONENT_NAME, path=build_dir)


def pydantic_form(
        model: Type[BaseModel],
        *,
        key: str = None,
        data: Dict = None,
        disabled: bool = False,
        readonly: bool = False,
) -> Tuple[Optional[BaseModel], bool]:
    """
    render a react-json-schema form by json schema from pydantic model
    default ui is material ui v5
    see details in frontend/
    :param model: the pydantic model type
    :param key: the elementId of the Form
    :param data: default value of the model.
    :param disabled: disable the ui
    :param readonly: enable the ui but readonly
    :return: (model instance: BaseModel, submitted: bool)
    model instance is None unless the form is submitted, get the pydantic model instance.
    this function use pydantic model to validate the result that form returns.
    """
    schema = model.model_json_schema()
    if key is None:
        key = model.__module__ + ":" + model.__name__
    result, submitted = jsonschema_form(
        key,
        schema,
        data=data,
        disabled=disabled,
        readonly=readonly,
    )
    if result is not None:
        return model(**result), submitted is True
    return result, submitted is True


def _pydantic_model_key(model: Type[BaseModel]) -> str:
    return f"{model.__module__}:{model.__qualname__}"


def pydantic_instance_form(
        instance: BaseModel,
        *,
        key: str = None,
        deep: bool = True,
        disabled: bool = False,
        readonly: bool = False,
) -> Tuple[Optional[BaseModel], bool]:
    """
    render a react-json-schema form by json schema from pydantic instance
    default ui is material ui v5
    :param instance: pydantic model instance
    :param key: the elementId of the Form
    :param deep: if deep is True, return instance's deep copy by updated values
    :param disabled: disable the ui
    :param readonly: enable the ui but readonly
    :return: (instance, submitted)
    instance is None unless the form is submitted, get the pydantic model instance.
    """
    data = instance.model_dump(exclude_defaults=False)
    model = type(instance)
    if key is None:
        key = model.__module__ + ":" + model.__name__
    schema = instance.model_json_schema()
    result, submitted = jsonschema_form(key, schema, data=data, disabled=disabled, readonly=readonly)
    if result is None:
        return None, submitted is True
    return instance.model_copy(update=result, deep=deep), submitted is True


def jsonschema_form(
        key: str,
        schema: Dict,
        *,
        data: Dict = None,
        disabled: bool = False,
        readonly: bool = False,
) -> Tuple[Optional[Dict], bool]:
    """
    render a react-json-schema form by raw json schema
    :param key: the elementId of the Form
    :param schema: the json schema
    :param data: default value of the schema
    :param disabled: disable the ui
    :param readonly: enable the ui but readonly
    :return: None unless the form is submitted, get the dict value of the formData
    """
    if data is None:
        data = {}
    with st.container(border=True):
        component_value = _component_func(
            key=key,
            schema=schema,
            formData=data,
            disabled=disabled,
            submitted=False,
            readonly=readonly,
        )
    if isinstance(component_value, dict):
        val, submitted = component_value.get("formData", data), component_value.get("submitted", False)
        return val, submitted
    return None, False
