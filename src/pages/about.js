import React from 'react';
import './about.css';

class About extends React.Component {
    render() {
        return (
            <div className="about" id="about" ref={this.props.reference}>
                <h1 >About</h1>
            </div>
        );
    }
}

export default About;