import React from 'react';
import './menu.css';
import Logo from '../images/logo.svg';

class Menu extends React.Component {

    render() {
        return (
            <div className="navbar">
                <a className="menu-item" href={`${window.location.origin}`}>
                    Home
                </a>
                <a className="menu-item" href={`${window.location.origin}#about`}>
                    About
                </a>
                <a className="menu-item" href={`${window.location.origin}#experience`}>
                    Experience
                </a>
                <a className="menu-item" href={`${window.location.origin}#projects`}>
                    Projects
                </a>
                <a className="menu-item" href={`${window.location.origin}#contact`}>
                    Contact
                </a>
            </div>
        )
    }
}

export default Menu;
