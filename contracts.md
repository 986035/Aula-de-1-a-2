# VAGA BLINDADA ROV - Contratos de Integração

## 📋 **Dados Mockados que serão substituídos por Backend Real**

### 🎯 **Frontend Mock Data (a ser removido)**
- `/src/data/mock.js` - Todos os dados estáticos do curso
- CTAs mockados que apenas fazem console.log
- Estatísticas hardcoded
- Informações do instrutor estáticas

---

## 🔄 **APIs Backend a Implementar**

### **1. Informações do Curso**
```
GET /api/course/info
Response: {
  product: { name, subtitle, price, oldPrice },
  hero: { announcement, title, subtitle, videoUrl },
  stats: [{ number, label }],
  benefits: [{ title, description }],
  courseContent: [{ icon, title, description }],
  bonuses: [{ icon, title, description }],
  instructor: { name, bio, experience, photo }
}
```

### **2. Lead Capture (Interesse)**
```
POST /api/leads/capture
Body: {
  name: string,
  email: string,
  phone: string,
  source: "hero" | "cta" | "footer"
}
Response: { success: boolean, leadId: string }
```

### **3. Checkout/Pagamento**
```
POST /api/checkout/create
Body: {
  customerName: string,
  customerEmail: string,
  customerPhone: string,
  source: string
}
Response: {
  checkoutUrl: string,
  paymentId: string
}
```

### **4. Webhook Pagamento**
```
POST /api/webhooks/payment
Body: { paymentData from Stripe }
Response: { received: true }
```

### **5. Analytics/Tracking**
```
POST /api/analytics/event
Body: {
  event: "page_view" | "cta_click" | "video_play" | "purchase",
  source: string,
  metadata: object
}
```

---

## 💳 **Sistema de Pagamento**

### **Stripe Integration**
- **Produto**: Curso VAGA BLINDADA ROV
- **Preço**: R$ 297,00
- **Método**: Checkout Session do Stripe
- **Webhook**: Confirmação automática de pagamento
- **Redirect**: Página de sucesso com acesso ao curso

### **Fluxo de Pagamento**
1. Usuário clica "Garantir Minha Vaga"
2. Coleta dados: nome, email, telefone
3. Cria sessão de checkout Stripe
4. Redireciona para Stripe Checkout
5. Webhook confirma pagamento
6. Envia email com acesso ao curso
7. Redireciona para página de sucesso

---

## 🎯 **Melhorias nos CTAs**

### **Variações de Botões de Ação**
```javascript
const ctaVariations = [
  "GARANTIR MINHA VAGA",
  "QUERO MINHA VAGA",
  "COMEÇAR AGORA",
  "GARANTIR ACESSO",
  "QUERO COMEÇAR",
  "INSCREVER-ME AGORA",
  "ADQUIRIR CURSO",
  "PROTEGER MINHA VAGA"
]
```

### **CTAs Contextuais**
- **Hero**: "GARANTIR MINHA VAGA" (urgência)
- **Benefícios**: "QUERO APRENDER ISSO" (desejo)
- **Conteúdo**: "QUERO TODO ESSE CONTEÚDO" (valor)
- **Bônus**: "GARANTIR TODOS OS BÔNUS" (escassez)
- **Instrutor**: "QUERO SER ORIENTADO" (autoridade)
- **CTA Final**: "NÃO QUERO PERDER ESSA CHANCE" (FOMO)

---

## 🗄️ **Modelos de Banco (MongoDB)**

### **Course**
```javascript
{
  _id: ObjectId,
  name: String,
  subtitle: String,
  price: Number,
  oldPrice: Number,
  currency: String,
  status: "active" | "inactive",
  createdAt: Date,
  updatedAt: Date
}
```

### **Lead**
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  phone: String,
  source: String,
  status: "new" | "contacted" | "converted",
  createdAt: Date,
  convertedAt: Date
}
```

### **Purchase**
```javascript
{
  _id: ObjectId,
  customerName: String,
  customerEmail: String,
  customerPhone: String,
  courseId: ObjectId,
  amount: Number,
  currency: String,
  paymentMethod: String,
  stripeSessionId: String,
  status: "pending" | "completed" | "failed",
  createdAt: Date,
  completedAt: Date
}
```

### **Analytics**
```javascript
{
  _id: ObjectId,
  event: String,
  source: String,
  metadata: Object,
  userAgent: String,
  ip: String,
  createdAt: Date
}
```

---

## 🔄 **Frontend Integration Changes**

### **Remover Mock Data**
1. Substituir `mockData` por chamadas API
2. Implementar loading states
3. Adicionar error handling
4. Implementar cache local (localStorage)

### **Novos Hooks React**
```javascript
// Custom hooks para API calls
useCoursInfo() // GET course data
useLeadCapture() // POST lead capture
useCheckout() // POST create checkout
useAnalytics() // POST track events
```

### **Estado da Aplicação**
```javascript
// Context para gerenciar estado global
const AppContext = {
  courseData: null,
  isLoading: boolean,
  error: string | null,
  user: null // se tiver login
}
```

---

## 🎯 **Funcionalidades Avançadas**

### **Lead Magnets**
- Pop-up com "Ebook Grátis: 10 Dicas ROV"
- Exit-intent popup
- Scroll percentage triggers

### **Social Proof**
- Contador de inscritos em tempo real
- Últimas compras (ticker)
- Depoimentos dinâmicos

### **Urgência/Escassez**
- Timer countdown
- "Restam apenas X vagas"
- "Últimas 48h com desconto"

---

## 🔧 **Integrações Adicionais**

### **Email Marketing**
- Mailchimp/ConvertKit integration
- Sequences automatizadas
- Segmentação por fonte

### **WhatsApp**
- Botão floating WhatsApp
- Mensagem pré-definida
- Link direto para atendimento

### **Analytics**
- Google Analytics 4
- Facebook Pixel
- Hotjar (heatmaps)

---

## 🚀 **Implementação Priority**

### **Fase 1 - Core Backend**
1. ✅ Modelos de dados
2. ✅ APIs básicas (course info, leads)
3. ✅ Integração Stripe
4. ✅ Webhook handling

### **Fase 2 - Frontend Integration** 
1. ✅ Remover mock data
2. ✅ Implementar API calls
3. ✅ Melhorar CTAs
4. ✅ Loading/error states

### **Fase 3 - Advanced Features**
1. ⏳ Analytics tracking
2. ⏳ Email integrations
3. ⏳ Social proof features
4. ⏳ WhatsApp integration

---

## 🎯 **Success Metrics**

### **KPIs a Trackear**
- **Conversion Rate**: Visitantes → Leads → Vendas
- **CTR**: Click-through rate dos CTAs
- **Video Engagement**: % que assiste o vídeo
- **Source Attribution**: Qual canal converte mais
- **Revenue**: MRR, LTV, AOV

### **A/B Tests Planejados**
- Variações de CTAs
- Cores dos botões
- Posicionamento de elementos
- Copy do hero section
- Preços e ofertas

---

Este contrato define toda a migração de mock para funcionalidade real, garantindo uma landing page que realmente vende e converte! 🚀