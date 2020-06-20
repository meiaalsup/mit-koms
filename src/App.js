import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [lee] = leeCount();

  leeCount(() => {
    fetch('/lee').then(res => res.json()).then(data => {
      return data['lee']
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">

        <div className="count">
          <p>Lee's KOMs: {lee}.</p>
        </div>
      </header>
    </div>
  );
}

export default App;
