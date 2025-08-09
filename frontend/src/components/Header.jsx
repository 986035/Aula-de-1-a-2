import React, { useState } from "react";
import { Button } from "./ui/button";
import { Menu, X, Target } from "lucide-react";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  const handlePurchase = () => {
    console.log("Navigate to purchase");
  };

  return (
    <header className="header-nav">
      <div className="container">
        <div className="nav-content">
          <div className="logo-section">
            <Target size={24} className="logo-icon" />
            <span className="logo-text">VAGA BLINDADA ROV</span>
          </div>
          
          <nav className={`nav-menu ${isMenuOpen ? 'nav-menu-open' : ''}`}>
            <button onClick={() => scrollToSection('benefits')} className="nav-link">
              O Curso
            </button>
            <button onClick={() => scrollToSection('content-section')} className="nav-link">
              Conteúdo
            </button>
            <button onClick={() => scrollToSection('instructor-section')} className="nav-link">
              Instrutor
            </button>
            <Button onClick={handlePurchase} className="btn-primary nav-cta">
              Garantir Vaga
            </Button>
          </nav>
          
          <button 
            className="btn-nav mobile-menu-toggle"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;