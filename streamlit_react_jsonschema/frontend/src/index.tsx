import React from "react"
import ReactJSONSchemaComponent from "./ReactJSONSchemaComponent"
import {createRoot} from "react-dom/client";


const node = document.getElementById('root')
if (node !== null) {
    const root = createRoot(node)
    root.render(
        <React.StrictMode>
            <ReactJSONSchemaComponent/>
        </React.StrictMode>
    )
}





