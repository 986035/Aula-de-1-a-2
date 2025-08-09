import React from "react";
import { Target } from "lucide-react";

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <div className="loading-icon">
          <Target size={48} className="animate-spin" />
        </div>
        <h2 className="loading-title">Carregando VAGA BLINDADA ROV</h2>
        <p className="loading-subtitle">Preparando o melhor conteúdo para você...</p>
      </div>
      
      <style jsx>{`
        .loading-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--bg-page);
        }
        
        .loading-content {
          text-align: center;
          max-width: 400px;
        }
        
        .loading-icon {
          margin-bottom: 2rem;
          color: #f1c40f;
        }
        
        .loading-title {
          font-family: 'SF Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 0.5rem;
          text-transform: uppercase;
          letter-spacing: 0.025em;
        }
        
        .loading-subtitle {
          color: var(--text-secondary);
          font-size: 1rem;
        }
        
        .animate-spin {
          animation: spin 2s linear infinite;
        }
        
        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
};

export default LoadingSpinner;