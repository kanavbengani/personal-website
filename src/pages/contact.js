import React from 'react';
import './contact.css';

class Contact extends React.Component {

    render() {
        return (
            <div className="contact" id="contact" ref={this.props.reference}>
                <h1>Contact</h1>
            </div>
        )
    }
}

export default Contact;