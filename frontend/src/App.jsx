import { useState } from "react";
import {
  Link,
  FileText,
  ShieldCheck,
  MessageCircle,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  Loader2,
} from "lucide-react";

import "./index.css";

const API_URL = "http://localhost:8000";

function App() {
  const [source, setSource] = useState("");
  const [language, setLanguage] = useState("english");

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  const [activeTab, setActiveTab] = useState("overview");

  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState([]);

  // --------------------------------------------------
  // Process video
  // --------------------------------------------------

  const analyzeVideo = async () => {
    if (!source.trim()) {
      alert("Please enter a YouTube URL or file path.");
      return;
    }

    setLoading(true);
    setData(null);

    try {
      const response = await fetch(`${API_URL}/process`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          source,
          language,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || "Failed to process video");
      }

      setData(result);

      setActiveTab("overview");
    } catch (error) {
      console.error(error);

      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Chat
  // --------------------------------------------------

  const sendQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    const userMessage = question;

    setChatMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setQuestion("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          question: userMessage,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || "Chat failed");
      }

      setChatMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: result.answer,
        },
      ]);
    } catch (error) {
      setChatMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${error.message}`,
        },
      ]);
    }
  };

  return (
    <div className="app">
      {/* ------------------------------------------------ */}
      {/* Header */}
      {/* ------------------------------------------------ */}

      <header className="header">
        <div className="brand">
          <div className="brand-icon">◉</div>

          <div>
            <h2>AI Video Assistant</h2>
            <span>Research & Intelligence</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Ready
        </div>
      </header>

      {/* ------------------------------------------------ */}
      {/* Hero */}
      {/* ------------------------------------------------ */}

      <main>
        <section className="hero">
          <div className="hero-badge">AI-POWERED VIDEO ANALYSIS</div>

          <h1>
            Turn any video into
            <span> actionable intelligence.</span>
          </h1>

          <p>
            Transcribe, summarize, verify factual claims, extract insights and
            chat with your content.
          </p>

          {/* Input */}

          <div className="input-card">
            <div className="input-row">
              <Link size={20} />

              <input
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="Paste YouTube URL or local file path..."
                disabled={loading}
              />
            </div>

            <div className="input-actions">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                disabled={loading}
              >
                <option value="english">English — Whisper</option>

                <option value="hinglish">Hinglish — Sarvam</option>
              </select>

              <button onClick={analyzeVideo} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 size={18} className="spin" />
                    Analyzing...
                  </>
                ) : (
                  <>Analyze Video</>
                )}
              </button>
            </div>
          </div>
        </section>

        {/* ------------------------------------------------ */}
        {/* Results */}
        {/* ------------------------------------------------ */}

        {data && (
          <section className="results">
            <div className="video-title">
              <span>ANALYSIS RESULT</span>

              <h2>{data.title}</h2>
            </div>

            {/* Tabs */}

            <div className="tabs">
              <button
                className={activeTab === "overview" ? "active" : ""}
                onClick={() => setActiveTab("overview")}
              >
                <FileText size={17} />
                Overview
              </button>

              <button
                className={activeTab === "claims" ? "active" : ""}
                onClick={() => setActiveTab("claims")}
              >
                <ShieldCheck size={17} />
                Fact Check
              </button>

              <button
                className={activeTab === "transcript" ? "active" : ""}
                onClick={() => setActiveTab("transcript")}
              >
                <FileText size={17} />
                Transcript
              </button>

              <button
                className={activeTab === "chat" ? "active" : ""}
                onClick={() => setActiveTab("chat")}
              >
                <MessageCircle size={17} />
                Chat
              </button>
            </div>

            {/* Overview */}

            {activeTab === "overview" && (
              <div className="overview-grid">
                <div className="main-card">
                  <h3>Summary</h3>

                  <div className="summary">{data.summary}</div>
                </div>

                <div className="side-column">
                  <InfoCard
                    title="Action Items"
                    icon={<CheckCircle2 size={18} />}
                    content={data.action_items}
                  />

                  <InfoCard
                    title="Key Decisions"
                    icon={<ShieldCheck size={18} />}
                    content={data.key_decisions}
                  />

                  <InfoCard
                    title="Open Questions"
                    icon={<HelpCircle size={18} />}
                    content={data.open_questions}
                  />
                </div>
              </div>
            )}

            {/* Claims */}

            {activeTab === "claims" && (
              <div className="claims-section">
                <div className="section-heading">
                  <div>
                    <span>FACT CHECKING</span>

                    <h2>Verified Claims</h2>
                  </div>

                  <div className="claim-count">
                    {data.verified_claims.length} claims
                  </div>
                </div>

                {data.verified_claims.map((item, index) => (
                  <ClaimCard key={index} item={item} index={index} />
                ))}
              </div>
            )}

            {/* Transcript */}

            {activeTab === "transcript" && (
              <div className="transcript-card">
                <h2>Transcript</h2>

                <p>{data.transcript}</p>
              </div>
            )}

            {/* Chat */}

            {activeTab === "chat" && (
              <div className="chat-card">
                <div className="chat-header">
                  <MessageCircle size={20} />

                  <div>
                    <h3>Chat with your video</h3>

                    <span>Ask questions about the content</span>
                  </div>
                </div>

                <div className="messages">
                  {chatMessages.length === 0 && (
                    <div className="empty-chat">
                      Ask something like:
                      <div className="suggestions">
                        <button
                          onClick={() =>
                            setQuestion("What are the main points discussed?")
                          }
                        >
                          What are the main points?
                        </button>

                        <button
                          onClick={() =>
                            setQuestion("What risks were discussed?")
                          }
                        >
                          What risks were discussed?
                        </button>
                      </div>
                    </div>
                  )}

                  {chatMessages.map((message, index) => (
                    <div
                      key={index}
                      className={
                        message.role === "user"
                          ? "message user"
                          : "message assistant"
                      }
                    >
                      {message.content}
                    </div>
                  ))}
                </div>

                <div className="chat-input">
                  <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        sendQuestion();
                      }
                    }}
                    placeholder="Ask about the video..."
                  />

                  <button onClick={sendQuestion}>Send</button>
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

// --------------------------------------------------
// Info Card
// --------------------------------------------------

function InfoCard({ title, icon, content }) {
  return (
    <div className="info-card">
      <div className="card-title">
        {icon}

        <h3>{title}</h3>
      </div>

      <div className="card-content">{content}</div>
    </div>
  );
}

// --------------------------------------------------
// Claim Card
// --------------------------------------------------

function ClaimCard({ item, index }) {
  const verification = item.verification || "";

  const verdict =
    verification.match(/VERDICT:\s*(.*)/)?.[1]?.trim() || "UNVERIFIED";

  let verdictClass = "unverified";

  if (verdict === "VERIFIED") {
    verdictClass = "verified";
  }

  if (verdict === "PARTIALLY VERIFIED") {
    verdictClass = "partial";
  }

  if (verdict === "CONTRADICTED") {
    verdictClass = "contradicted";
  }

  const Icon =
    verdict === "VERIFIED"
      ? CheckCircle2
      : verdict === "CONTRADICTED"
        ? XCircle
        : verdict === "PARTIALLY VERIFIED"
          ? AlertTriangle
          : HelpCircle;

  return (
    <div className="claim-card">
      <div className="claim-top">
        <span className="claim-number">CLAIM {index + 1}</span>

        <span className={`verdict ${verdictClass}`}>
          <Icon size={15} />

          {verdict}
        </span>
      </div>

      <h3>{item.claim}</h3>

      <div className="verification">{verification}</div>

      <div className="sources">
        <h4>Sources</h4>

        {item.sources.map((source, index) => (
          <a key={index} href={source.url} target="_blank" rel="noreferrer">
            {source.title}
          </a>
        ))}
      </div>
    </div>
  );
}

export default App;
