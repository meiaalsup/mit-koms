import React from 'react';
import './App.css';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      results: []
    };
  }

  componentDidMount() {
    fetch("koms", {
      method: "GET",
    }).then(response => response.json())
      .then(json => {
        this.setState({results: json})
        console.log(json)
      })
  }

  

  render() {
    let people = Object.keys(this.state.results)
    let komCounts = people.map(
      (name, index) => 
        <div key={index} className="count">
          <p>{name}'s KOMs: {this.state.results[name]}.</p>
        </div>
    );

    return (
      <div className="App">
        <header className="App-header">
          <div className="countwrapper">
            {komCounts}
          </div>

        </header>
      </div>
    );
  }

}

export default App;
