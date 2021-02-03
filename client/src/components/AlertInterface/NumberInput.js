import React, { Component, useState } from 'react';
import { Button } from 'semantic-ui-react';
import "./NumberInput.css"
import PhoneNumberInput, { isPossiblePhoneNumber } from 'react-phone-number-input'
import 'react-phone-number-input/style.css'

export class NumberInput extends Component {
    constructor(props) {
    super(props);

    this.state = {
      value: "",
      showErrorText: false,
      showLocationInput: false,
      _huge: true
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleKeyUp = this.handleKeyUp.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.beResponsive = this.beResponsive.bind(this);
  }
  
  componentDidMount() {
    var x = window.matchMedia("(max-width: 500px)")
    this.beResponsive(x)
    x.addListener(this.beResponsive)
  }

  beResponsive(x){
    console.log(x)
    var element = document.getElementsByClassName("PhoneInput")[0]
    this.setState({
      huge:!x.matches
    })
  }

  keyCodeIsNumber(code) {
    return (code >= 48 && code <= 57) || (code >= 96 && code <= 105);
  }

  handleChange(value) {
    this.setState({ 
      value: value
    })
  }

  handleKeyDown(event) {
    if (event.key === 'Enter') { // enter
      this.handleSubmit()
    }
    console.log(event.key)
  }

  handleKeyUp(event) {
    if (this.state.deleteOnUp) {
      this.handleChange(event);
    }
  }

  handleSubmit(event){
    if (!isPossiblePhoneNumber(this.state.value)){
      this.setState({showErrorText: true})
    }
    else{
      this.props.displayForm(true)
      this.props.retrieveNumber(this.state.value)
      this.setState({showErrorText: false})
    }
  }

  render() {
    return (
      <div className="NumberInput">
        <div className="input-container">
          <PhoneNumberInput 
            countries={["US"]}
            value={this.state.value}
            onChange={this.handleChange} 
            limitMaxLength={true}
            addInternationalOption={false}
            className={this.state.huge ? "ui input huge" : "ui input medium"}
            id="number-input"
            onKeyPress={this.handleKeyDown}
          />
          <Button className="submit-btn" onClick={this.handleSubmit}>Go</Button>
        </div>
        {this.state.showErrorText ? <p className="error"> Not a valid phone number!</p> : null}
      </div>
    );
  }
}

export default NumberInput;