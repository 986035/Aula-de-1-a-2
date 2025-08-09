import React from "react";
import { Target, MessageCircle, Mail } from "lucide-react";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-brand">
            <div className="footer-logo">
              <Target size={32} />
              <span className="logo-text">VAGA BLINDADA ROV</span>
            </div>
            <p className="footer-description body-small">
              O guia completo para conquistar sua vaga de trainee ROV no mercado offshore.
            </p>
          </div>
          
          <div className="footer-links">
            <div className="footer-section">
              <h4 className="footer-title heading-3">Curso</h4>
              <ul className="footer-list">
                <li><a href="#benefits" className="footer-link">Benefícios</a></li>
                <li><a href="#content" className="footer-link">Conteúdo</a></li>
                <li><a href="#bonus" className="footer-link">Bônus</a></li>
                <li><a href="#instructor" className="footer-link">Instrutor</a></li>
              </ul>
            </div>
            
            <div className="footer-section">
              <h4 className="footer-title heading-3">Contato</h4>
              <div className="footer-contact">
                <div className="contact-item">
                  <MessageCircle size={16} />
                  <span className="caption">Acesso direto ao instrutor</span>
                </div>
                <div className="contact-item">
                  <Mail size={16} />
                  <span className="caption">Suporte via email</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <div className="footer-divider"></div>
          <div className="footer-bottom-content">
            <p className="caption">
              © 2025 Vaga Blindada ROV. Todos os direitos reservados.
            </p>
            <div className="footer-legal">
              <a href="#" className="footer-link caption">Política de Privacidade</a>
              <a href="#" className="footer-link caption">Termos de Uso</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;