import React, { useEffect, useState } from "react";
import { CheckCircle, Download, MessageCircle, Calendar, ArrowRight, Loader } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { usePaymentStatus, useAnalytics } from "../hooks/useApi";
import { getUrlParameter } from "../hooks/useApi";

const SuccessPage = () => {
  const [sessionId, setSessionId] = useState(null);
  const [paymentData, setPaymentData] = useState(null);
  const { pollPaymentStatus, isChecking } = usePaymentStatus();
  const { trackEvent } = useAnalytics();
  const [statusMessage, setStatusMessage] = useState("Verificando pagamento...");
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    const sessionIdFromUrl = getUrlParameter('session_id');
    if (sessionIdFromUrl) {
      setSessionId(sessionIdFromUrl);
      checkPayment(sessionIdFromUrl);
    } else {
      setStatusMessage("Sessão de pagamento não encontrada");
    }
  }, []);

  const checkPayment = async (sessionId) => {
    try {
      setStatusMessage("Verificando seu pagamento...");
      const data = await pollPaymentStatus(sessionId);
      
      if (data.payment_status === 'paid') {
        setPaymentData(data);
        setIsSuccess(true);
        setStatusMessage("Pagamento confirmado com sucesso!");
        
        // Track successful conversion
        await trackEvent('conversion_success', 'payment_success', {
          transaction_id: data.transaction_id,
          amount: data.amount_total,
          currency: data.currency
        });
      }
    } catch (error) {
      console.error('Payment verification error:', error);
      setStatusMessage("Erro ao verificar pagamento. Por favor, entre em contato conosco.");
    }
  };

  const nextSteps = [
    {
      icon: MessageCircle,
      title: "Acesso ao Telegram",
      description: "Você receberá um convite para o canal exclusivo do curso",
      action: "Aguardar convite"
    },
    {
      icon: Download,
      title: "Materiais do Curso",
      description: "Download de apostilas, templates e recursos extras",
      action: "Acessar materiais"
    },
    {
      icon: Calendar,
      title: "Cronograma de Estudos",
      description: "Seu plano personalizado para dominar o conteúdo ROV",
      action: "Ver cronograma"
    }
  ];

  return (
    <div className="success-page">
      <div className="success-bg-overlay"></div>
      <div className="container">
        <div className="success-content">
          
          {/* Status Card */}
          <Card className="status-card">
            <CardContent className="p-8 text-center">
              {isChecking && !isSuccess ? (
                <div className="status-checking">
                  <Loader size={48} className="animate-spin text-blue-500 mb-4" />
                  <h2 className="heading-2">{statusMessage}</h2>
                  <p className="body-medium text-gray-600">
                    Aguarde enquanto confirmamos seu pagamento...
                  </p>
                </div>
              ) : isSuccess ? (
                <div className="status-success">
                  <CheckCircle size={64} className="text-green-500 mb-4 mx-auto" />
                  <h1 className="heading-hero text-green-600 mb-4">
                    Parabéns! Compra Realizada com Sucesso! 🎉
                  </h1>
                  <p className="body-large mb-6">
                    Bem-vindo ao <strong>VAGA BLINDADA ROV</strong>! 
                    Você agora tem acesso completo ao curso.
                  </p>
                  
                  {paymentData && (
                    <div className="payment-details">
                      <div className="detail-item">
                        <span>Valor pago:</span>
                        <strong>{paymentData.currency} {paymentData.amount_total.toFixed(2)}</strong>
                      </div>
                      <div className="detail-item">
                        <span>Transação:</span>
                        <strong>#{paymentData.transaction_id?.slice(-8)}</strong>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="status-error">
                  <div className="error-icon text-red-500 mb-4">❌</div>
                  <h2 className="heading-2 text-red-600">{statusMessage}</h2>
                  <p className="body-medium">
                    Se você fez o pagamento, entre em contato conosco para resolvermos rapidamente.
                  </p>
                  <Button 
                    onClick={() => window.location.href = "/"} 
                    className="btn-primary mt-4"
                  >
                    Voltar ao Início
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Next Steps - Only show if payment is successful */}
          {isSuccess && (
            <div className="next-steps">
              <h2 className="heading-1 text-center mb-6">Próximos Passos</h2>
              
              <div className="steps-grid">
                {nextSteps.map((step, index) => (
                  <Card key={index} className="step-card voice-card accent-blue">
                    <CardContent className="p-6">
                      <div className="step-number">{index + 1}</div>
                      <step.icon className="step-icon text-blue-500" size={32} />
                      <h3 className="voice-card-title">{step.title}</h3>
                      <p className="voice-card-description">{step.description}</p>
                      <div className="step-action">
                        <span className="action-text">{step.action}</span>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
              
              <div className="final-message">
                <Card className="message-card voice-card accent-green">
                  <CardContent className="p-6 text-center">
                    <h3 className="voice-card-title">🚀 Sua Jornada ROV Começa Agora!</h3>
                    <p className="voice-card-description">
                      Você receberá um email em breve com todas as instruções de acesso. 
                      Bem-vindo à elite dos profissionais ROV offshore!
                    </p>
                    <Button 
                      onClick={() => window.location.href = "/"} 
                      className="btn-primary mt-4"
                    >
                      Voltar ao Site
                      <ArrowRight size={16} className="ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <style jsx>{`
        .success-page {
          min-height: 100vh;
          background: var(--bg-page);
          position: relative;
        }
        
        .success-bg-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, 
            rgba(46, 204, 113, 0.1) 0%, 
            rgba(52, 152, 219, 0.1) 100%);
          z-index: -1;
        }
        
        .success-content {
          padding: 2rem 0;
          max-width: 1000px;
          margin: 0 auto;
        }
        
        .status-card {
          margin-bottom: 3rem;
        }
        
        .payment-details {
          background: rgba(46, 204, 113, 0.1);
          border-radius: 0.5rem;
          padding: 1rem;
          margin-top: 1rem;
          display: flex;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 1rem;
        }
        
        .detail-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.25rem;
        }
        
        .steps-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
          margin-bottom: 3rem;
        }
        
        .step-card {
          position: relative;
        }
        
        .step-number {
          position: absolute;
          top: -10px;
          right: -10px;
          background: #3498db;
          color: white;
          width: 30px;
          height: 30px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          font-size: 0.875rem;
        }
        
        .step-icon {
          margin-bottom: 1rem;
        }
        
        .step-action {
          margin-top: 1rem;
          padding-top: 1rem;
          border-top: 1px solid var(--border-light);
        }
        
        .action-text {
          font-family: 'SF Mono', monospace;
          font-size: 0.75rem;
          text-transform: uppercase;
          color: var(--accent-blue-400);
          font-weight: 500;
        }
        
        .error-icon {
          font-size: 3rem;
        }
        
        @media (max-width: 768px) {
          .success-content {
            padding: 1rem;
          }
          
          .payment-details {
            flex-direction: column;
            text-align: center;
          }
          
          .steps-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default SuccessPage;