# VAGA BLINDADA ROV - Landing Page

## 🚀 Como Personalizar Facilmente

### 1. **Alterando Imagens de Fundo**
Edite o arquivo `/src/data/config.js`:
```javascript
images: {
  heroBackground: "URL_DA_SUA_IMAGEM_HERO",
  benefitsBackground: "URL_DA_SUA_IMAGEM_BENEFICIOS", 
  contentBackground: "URL_DA_SUA_IMAGEM_CONTEUDO",
  instructorBackground: "URL_DA_SUA_IMAGEM_INSTRUTOR"
}
```

### 2. **Modificando Textos e Conteúdo**
Edite o arquivo `/src/data/mock.js`:
- **Hero**: título, subtítulo, CTAs
- **Benefícios**: adicionar/remover/editar benefícios
- **Conteúdo do curso**: modificar itens inclusos
- **Bônus**: personalizar bônus oferecidos
- **Instrutor**: alterar informações

### 3. **Adicionando Vídeo Real**
No arquivo `/src/data/config.js`:
```javascript
video: {
  placeholder: false, // Mudar para false
  embedUrl: "https://www.youtube.com/embed/SEU_VIDEO_ID",
  thumbnailUrl: "URL_DA_THUMBNAIL" // opcional
}
```

### 4. **Configurações de Contato**
No arquivo `/src/data/config.js`:
```javascript
contact: {
  telegram: "@seutelegram",
  email: "seu@email.com", 
  phone: "+55 11 99999-9999"
}
```

### 5. **Cores e Design**
Modifique as variáveis CSS em `/src/App.css`:
```css
:root {
  --bg-page: #FFF9F2; /* Cor de fundo principal */
  --text-primary: #232323; /* Cor do texto */
  /* Cores dos cards */
  --accent-blue-200: #E4EDF8;
  --accent-purple-200: #F9E8FA;
  /* etc... */
}
```

## 📁 Estrutura de Arquivos

```
src/
├── components/
│   ├── LandingPage.jsx    # Componente principal
│   ├── Header.jsx         # Cabeçalho
│   └── Footer.jsx         # Rodapé
├── data/
│   ├── mock.js           # Conteúdo editável
│   └── config.js         # Configurações (imagens, vídeo, etc)
├── App.css              # Estilos (cores, tipografia)
└── App.js               # Aplicação principal
```

## 🎨 Imagens Incluídas

1. **Hero**: Plataforma petrolífera offshore (impacto visual)
2. **Benefícios**: Plataforma em águas brasileiras (contexto local)
3. **Conteúdo**: Equipamentos subaquáticos profissionais
4. **Instrutor**: Mergulhador profissional (experiência técnica)

## 🔧 Personalizações Rápidas

### Alterar Preço
```javascript
// Em mock.js
product: {
  price: "R$ 397,00",
  oldPrice: "R$ 597,00"
}
```

### Adicionar/Remover Seções
Edite `LandingPage.jsx` para adicionar novas seções ou remover existentes.

### Modificar Botões CTA
```javascript
// Em mock.js
hero: {
  ctaPrimary: "Seu Novo Texto",
  ctaSecondary: "Outro Texto"
}
```

## 📱 Responsividade
A página é totalmente responsiva e se adapta a:
- Desktop (1280px+)
- Tablet (768px-1279px) 
- Mobile (<768px)

## 🎯 Funcionalidades Implementadas
- ✅ Header fixo com navegação suave
- ✅ Hero com espaço para vídeo
- ✅ Backgrounds com imagens offshore
- ✅ Cards coloridos organizados
- ✅ Seção de instrutor destacada
- ✅ CTAs estratégicos
- ✅ Footer completo
- ✅ Animações suaves
- ✅ Fácil personalização

## 🚀 Próximos Passos
1. Substituir dados mockados por backend real
2. Integrar sistema de pagamento
3. Adicionar analytics (GA4, Facebook Pixel)
4. Implementar formulários de captura
5. Adicionar chat ou WhatsApp integration