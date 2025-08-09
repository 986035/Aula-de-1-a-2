import React, { useEffect } from "react";
import { XCircle, ArrowLeft, MessageCircle, Mail } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { useAnalytics } from "../hooks/useApi";

const CancelPage = () => {
  const { trackEvent } = useAnalytics();

  useEffect(() => {
    // Track cancellation
    trackEvent('payment_cancelled', 'stripe_cancel');
  }, [trackEvent]);

  const handleBackToSite = () => {
    trackEvent('return_from_cancel', 'cancel_page');
    window.location.href = "/";
  };

  const contactOptions = [
    {
      icon: MessageCircle,
      title: "WhatsApp",
      description: "Tire suas dúvidas pelo WhatsApp",
      action: "Chamar no WhatsApp",
      link: "https://wa.me/5511999999999" // Replace with real WhatsApp
    },
    {
      icon: Mail,
      title: "Email",
      description: "Envie suas perguntas por email",
      action: "Enviar Email",
      link: "mailto:contato@vagablindadarov.com" // Replace with real email
    }
  ];

  return (
    <div className="cancel-page">
      <div className="cancel-bg-overlay"></div>
      <div className="container">
        <div className="cancel-content">
          
          {/* Main Cancel Card */}
          <Card className="cancel-card">
            <CardContent className="p-8 text-center">
              <XCircle size={64} className="text-orange-500 mb-4 mx-auto" />
              
              <h1 className="heading-hero text-orange-600 mb-4">
                Pagamento Cancelado
              </h1>
              
              <p className="body-large mb-6 text-gray-600">
                Não se preocupe! Seu pagamento foi cancelado e nenhum valor foi cobrado.
                Você pode tentar novamente a qualquer momento.
              </p>
              
              <div className="cancel-reasons">
                <h3 className="heading-3 mb-4">Por que as pessoas cancelam?</h3>
                <div className="reasons-list">
                  <div className="reason-item">
                    <span className="reason-icon">💭</span>
                    <span>Precisam conversar com alguém primeiro</span>
                  </div>
                  <div className="reason-item">
                    <span className="reason-icon">💳</span>
                    <span>Problemas com cartão de crédito</span>
                  </div>
                  <div className="reason-item">
                    <span className="reason-icon">❓</span>
                    <span>Dúvidas sobre o conteúdo do curso</span>
                  </div>
                </div>
              </div>
              
              <div className="cancel-actions">
                <Button onClick={handleBackToSite} className="btn-primary">
                  <ArrowLeft size={16} className="mr-2" />
                  Voltar ao Curso
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Special Offer Card */}
          <Card className="offer-card voice-card accent-orange">
            <CardContent className="p-6 text-center">
              <h2 className="voice-card-title">🎯 Oferta Especial por Tempo Limitado</h2>
              <p className="voice-card-description mb-4">
                Que tal conversar com nosso time antes de decidir? 
                Podemos esclarecer todas as suas dúvidas sobre o curso ROV!
              </p>
              
              <div className="contact-options">
                {contactOptions.map((option, index) => (
                  <div key={index} className="contact-option">
                    <option.icon className="contact-icon" size={24} />
                    <div className="contact-info">
                      <strong className="contact-title">{option.title}</strong>
                      <p className="contact-description">{option.description}</p>
                    </div>
                    <a 
                      href={option.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="contact-button"
                      onClick={() => trackEvent('contact_click', 'cancel_page', { method: option.title.toLowerCase() })}
                    >
                      {option.action}
                    </a>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Guarantee Card */}
          <Card className="guarantee-card voice-card accent-green">
            <CardContent className="p-6 text-center">
              <h3 className="voice-card-title">🔒 Nossa Garantia</h3>
              <p className="voice-card-description">
                <strong>100% Seguro:</strong> Pagamento processado pelo Stripe, a mesma tecnologia 
                usada por empresas como Spotify e Uber. Seus dados estão protegidos e você pode 
                comprar com total tranquilidade.
              </p>
            </CardContent>
          </Card>

        </div>
      </div>
      
      <style jsx>{`
        .cancel-page {
          min-height: 100vh;
          background: var(--bg-page);
          position: relative;
        }
        
        .cancel-bg-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, 
            rgba(230, 126, 34, 0.1) 0%, 
            rgba(231, 76, 60, 0.1) 100%);
          z-index: -1;
        }
        
        .cancel-content {
          padding: 2rem 0;
          max-width: 800px;
          margin: 0 auto;
        }
        
        .cancel-card {
          margin-bottom: 2rem;
        }
        
        .cancel-reasons {
          background: rgba(230, 126, 34, 0.1);
          border-radius: 0.5rem;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }
        
        .reasons-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        
        .reason-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          text-align: left;
        }
        
        .reason-icon {
          font-size: 1.25rem;
          flex-shrink: 0;
        }
        
        .cancel-actions {
          margin-top: 2rem;
        }
        
        .offer-card {
          margin-bottom: 2rem;
        }
        
        .contact-options {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .contact-option {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          background: rgba(255, 255, 255, 0.5);
          border-radius: 0.5rem;
          text-align: left;
        }
        
        .contact-icon {
          color: var(--accent-orange-400);
          flex-shrink: 0;
        }
        
        .contact-info {
          flex: 1;
        }
        
        .contact-title {
          display: block;
          font-size: 0.875rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
        }
        
        .contact-description {
          font-size: 0.75rem;
          color: var(--text-secondary);
          margin: 0;
        }
        
        .contact-button {
          background: var(--accent-orange-400);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 1rem;
          text-decoration: none;
          font-size: 0.75rem;
          font-weight: 500;
          transition: all 0.2s ease;
        }
        
        .contact-button:hover {
          background: #a0621a;
          transform: scale(1.05);
        }
        
        .guarantee-card {
          margin-bottom: 2rem;
        }
        
        @media (max-width: 768px) {
          .cancel-content {
            padding: 1rem;
          }
          
          .contact-option {
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
          }
          
          .contact-info {
            text-align: center;
          }
        }
      `}</style>
    </div>
  );
};

export default CancelPage;