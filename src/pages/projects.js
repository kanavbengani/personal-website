import React from 'react';
import './projects.css';

class Projects extends React.Component {

    render() {
        return (
            <div className="projects" id="projects" ref={this.props.reference}>
                <h1>Projects</h1>
            </div>
        )
    }
}

export default Projects;