import {Streamlit, StreamlitComponentBase, withStreamlitConnection,} from "streamlit-component-lib"
import React, {ReactNode} from "react"
import {RJSFSchema} from '@rjsf/utils';
import {IChangeEvent, withTheme} from "@rjsf/core"
import {Theme} from '@rjsf/mui'
import validator from '@rjsf/validator-ajv8';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// my first try on TypeScript, React Component and Streamlit Component.
// coding, testing while learning.
// I apologize in advance for any bugs caused by my lack of proficiency.

// Define the State
// Seems React-Component use Generic state interface to both define the component properties
// and manage state change events.
interface State {
    formData: object
}


/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class ReactJSONSchemaComponent extends StreamlitComponentBase<State> {
    // fromData implements State interface?
    // ts can define interface with properties only, cool!
    formData = {}

    // prepare none state container for form data
    tempData: null | object = null
    // detect the form height change
    frameHeight = 0

    rjsRef: React.RefObject<any> = React.createRef()

    public render = (): ReactNode => {
        // Arguments that are passed to the plugin in Python are accessible
        // via `this.props.args`. Here, we access the "name" arg.
        const key = this.props.args["key"]
        const disabled = this.props.args["disabled"]
        const readonly = this.props.args["readonly"]
        // get json schema
        const schema: RJSFSchema = this.props.args["schema"]
        this.formData = this.props.args["default"] ?? {}
        if (this.tempData === null) {
            this.tempData = this.formData
        }

        // Streamlit sends us a theme object via props that we can use to ensure
        // that our component has visuals that match the active theme in a
        // streamlit app.
        const {theme} = this.props

        // define theme mode of mui
        // Perhaps there are more properties about the Theme that can be aligned.
        const baseMode = theme?.base === "light" ? "light" : "dark"
        const muiTheme = createTheme({
            palette: {
                mode: baseMode,
            },
        });


        const Form = withTheme(Theme)
        const rendered = <ThemeProvider theme={muiTheme}>
            <CssBaseline/>
            <Form
                id={key}
                ref={this.rjsRef}
                formData={this.tempData}
                schema={schema}
                validator={validator}
                onChange={this._onChange}
                onSubmit={this._onSubmit}
                disabled={disabled}
                readonly={readonly}
            />
        </ThemeProvider>

        return (
            rendered
        )
    }

    private _onChange = (event: IChangeEvent) => {
        // detect height on change.
        // json schema form may change height when add item to array or dict
        this.updateIframeHeight()
        this.tempData = event.formData
    }

    private _onSubmit = () => {
        Streamlit.setComponentValue({formData: this.tempData, submitted: true})
    }

    componentDidMount() {
        this.updateIframeHeight()
    }

    private updateIframeHeight() {
        // `?.` very cool
        const offsetHeight = this.rjsRef.current?.formElement?.current?.offsetHeight;
        if (offsetHeight && offsetHeight !== this.frameHeight) {
            this.frameHeight = offsetHeight
            // a little higher for paddings
            Streamlit.setFrameHeight(offsetHeight + 100)
        }
    }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(ReactJSONSchemaComponent)
