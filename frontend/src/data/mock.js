import { BookOpen, Users, Download, Award, Clock, CheckCircle, MessageCircle, Target, FileText, Video, Calendar } from "lucide-react";

export const mockData = {
  product: {
    name: "VAGA BLINDADA ROV",
    subtitle: "Tudo o que você precisa para proteger sua vaga dos concorrentes. O guia completo para conquistar uma vaga de trainee de ROV no mercado offshore.",
    price: "R$ 147,00",
    oldPrice: "R$ 297,00"
  },
  
  // Easy to modify content
  hero: {
    announcement: "Vagas Limitadas • Acesso Prioritário",
    title: "VAGA BLINDADA ROV",
    subtitle: "Tudo o que você precisa para proteger sua vaga dos concorrentes. O guia completo para conquistar uma vaga de trainee de ROV no mercado offshore.",
    videoText: "▶ Assista ao vídeo de apresentação",
    ctaPrimary: "Garantir Minha Vaga",
    ctaSecondary: "Conhecer o Método"
  },
  
  stats: [
    { number: "15+", label: "Anos de Experiência" },
    { number: "10", label: "Aulas Completas" },
    { number: "100%", label: "Método Prático" }
  ],
  
  benefits: [
    {
      title: "Mercado Offshore e ROV",
      description: "Como funciona o mercado offshore e onde o ROV atua. Entenda as oportunidades reais do setor."
    },
    {
      title: "Habilidades Valorizadas",
      description: "Quais habilidades as empresas realmente valorizam nos candidatos a trainee ROV."
    },
    {
      title: "Sistemas e Ferramentas",
      description: "Os principais sensores, ferramentas e sistemas usados no ROV que você precisa conhecer."
    },
    {
      title: "Currículo Profissional",
      description: "Como montar um currículo profissional mesmo sendo iniciante, destacando seus pontos fortes."
    },
    {
      title: "Entrevistas e Seleções",
      description: "Dicas práticas para entrevistas e processos seletivos das principais empresas offshore."
    },
    {
      title: "Vantagem Competitiva",
      description: "O principal: como proteger a SUA vaga dos concorrentes e se destacar no mercado."
    }
  ],
  
  targetAudience: [
    "Jovens técnicos que querem entrar no setor offshore",
    "Quem está iniciando na área e quer começar com vantagem",
    "Quem busca um guia completo e direto para conquistar sua vaga",
    "Técnicos em elétrica, mecânica, automação, mecatrônica ou áreas correlatas"
  ],
  
  courseContent: [
    {
      icon: Video,
      title: "10 Aulas em Vídeo",
      description: "Organizadas passo a passo para seu aprendizado progressivo"
    },
    {
      icon: FileText,
      title: "Apostilas e Slides",
      description: "Materiais complementares para reforçar o aprendizado"
    },
    {
      icon: Download,
      title: "Modelo de Currículo",
      description: "Pronto para edição, otimizado para o mercado offshore"
    },
    {
      icon: CheckCircle,
      title: "Checklists de Preparação",
      description: "Para você não esquecer nenhum detalhe importante"
    },
    {
      icon: Award,
      title: "Certificado de Conclusão",
      description: "10 horas de certificação para seu currículo"
    },
    {
      icon: MessageCircle,
      title: "Acesso ao Instrutor",
      description: "Canal direto no Telegram para tirar dúvidas"
    }
  ],
  
  bonuses: [
    {
      icon: Target,
      title: "Canal de Vagas Reais",
      description: "Canal fechado com alertas de vagas reais do mercado offshore"
    },
    {
      icon: Users,
      title: "Lista de Empresas",
      description: "Lista completa de empresas que contratam profissionais de ROV"
    },
    {
      icon: Calendar,
      title: "Cronograma de Estudos",
      description: "Para te manter no foco e organizar seu tempo de estudo"
    },
    {
      icon: Clock,
      title: "Atualizações Gratuitas",
      description: "Sempre que o curso for ampliado, você recebe as atualizações"
    }
  ],
  
  instructor: {
    name: "Leandro Pinheiro",
    bio: "Técnico mecatrônico com mais de 15 anos de experiência no setor offshore, especializado em sistemas de ROV.",
    experience: "Começou como técnico de ferramentas, evoluiu para piloto e hoje é referência em treinamento de novos profissionais."
  },
  
  // Customizable texts
  sections: {
    benefits: {
      title: "O que você vai aprender",
      subtitle: "Conteúdo completo e prático para se destacar no mercado offshore"
    },
    target: {
      title: "Para quem é esse curso?",
      cardTitle: "Técnicos de Todas as Áreas",
      cardDescription: "Elétrica, Mecânica, Automação, Mecatrônica e áreas correlatas"
    },
    content: {
      title: "O que você recebe ao se inscrever",
      subtitle: "Conteúdo completo para sua preparação"
    },
    bonus: {
      badge: "BÔNUS EXCLUSIVOS",
      title: "Vantagens adicionais para os primeiros inscritos"
    },
    instructor: {
      title: "Sobre o Instrutor"
    },
    cta: {
      title: "Não deixe sua oportunidade escapar",
      subtitle: "Os primeiros inscritos terão acompanhamento especial e acesso prioritário às atualizações do curso.",
      urgency: "Vagas limitadas para o grupo com acesso direto ao instrutor",
      button: "Garantir Minha Vaga Agora"
    }
  }
};