import React from 'react';
import './App.css'
import {SERVER_URL} from './config';
import both from './images/both.jpeg'
import lee_gu from './images/lee_gu.jpeg'
import miles_bread from './images/miles_bread.jpeg'

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      results: []
    };
  }

  componentDidMount() {
    fetch(SERVER_URL + "/koms", {
      method: "GET",
      mode: 'no-cors',
    }).then(response => response.json())
      .then(json => {
        this.setState({ results: json })
        console.log(json)
      })
  }



  render() {
    let people = Object.keys(this.state.results)
    console.log(this.state.results)
    let komCounts = people.map(
      (name, index) =>
        <div key={index} className="count">
          <p>{name}'s KOMs: {this.state.results[name]}.</p>
        </div>
    );

    return (
      <div className="App">
        <header className="App-header">
          <div className="image-box">
            <img className='some-image' src={lee_gu} alt='Lee eating Gu' />
            <img className='some-image' src={both}
                 alt='Lee looking back at Miles' />
            <img className='some-image' src={miles_bread} 
                 alt='Miles eating a sandwich'/>
          </div>
          <div className="countwrapper">
            {komCounts}
          </div>
        </header>
      </div>
    );
  }

}

export default App;
