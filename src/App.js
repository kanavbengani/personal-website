import React from 'react';
import Menu from './pages/menu';
import About from './pages/about';
import Experience from './pages/experience';
import Projects from './pages/projects';
import Contact from './pages/contact';

import './app.css';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.about = React.createRef();
    this.experience = React.createRef();
    this.projects = React.createRef();
    this.contact = React.createRef();
  }

  navigate = (location) => this[location].current.scrollIntoView({ behavior: 'smooth' });

  render() {
    return (
      <div className="app" >
        <Menu navigate={this.navigate} />
        <About reference={this.about} />
        <Experience reference={this.experience} />
        <Projects reference={this.projects} />
        <Contact reference={this.contact} />
      </div>
    );
  }
}

export default App;
