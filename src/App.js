import React from 'react';
import './App.css';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      lee: 0,
      miles: 0,
    };
  }

  componentDidMount() {
    fetch("koms", {
      method: "GET",
    }).then(response => response.json())
      .then(json => {
        this.setState({lee: json.lee, miles: json.miles})
        console.log(json)
      })
  }

  

  render() {

    return (
      <div className="App">
        <header className="App-header">

          <div className="count">
            <p>Lee's KOMs: {this.state.lee}.</p>
            <p>Miles's KOMs: {this.state.miles}.</p>
          </div>
        </header>
      </div>
    );
  }

}

export default App;
