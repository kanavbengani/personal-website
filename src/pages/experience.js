import React from 'react';
import './experience.css';

class Experience extends React.Component {

    render() {
        return (
            <div className="experience" id="experience" ref={this.props.reference}>
                <h1>Experience</h1>
            </div>
        )
    }
}

export default Experience;