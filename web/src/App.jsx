import "./App.css";
import { useState, useEffect } from "react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css";
// import { Gitgraph } from "@gitgraph/react";

import {
  ChatContainer,
  MessageList,
  Message,
  Avatar,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";

import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import FormRange from "react-bootstrap/FormRange";
import Modal from "react-bootstrap/Modal";

function App() {
  const [data, setData] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [genre, setGenre] = useState("Fantasy");
  const [temperature, setTemperature] = useState(0.0);
  const [model, setModel] = useState("gpt-3.5-turbo");
  const [isLoading, setIsLoading] = useState(false);
  const [characters, setCharacters] = useState();
  const [showImageModal, setShowImageModal] = useState(false);
  const [characterImages, setCharacterImages] = useState({});
  const [isGeneratingImages, setIsGeneratingImages] = useState(false);

  useEffect(() => {
    // Fetch initial data or previous messages if needed
  }, []);

  const parseCharacters = (message) => {
    // Extract character information from the message
    console.log("Raw message:", message); // Debug log

    const characterSection = message
      .split("Characters:\n")[1]
      ?.split("\n\nPlot:")[0];
    console.log("Character section:", characterSection); // Debug log

    if (!characterSection) {
      console.log("No character section found"); // Debug log
      return [];
    }

    const parsedCharacters = characterSection
      .split("\n\n") // Split by double newline to get each character block
      .map((block) => {
        const nameMatch = block.match(/Name:\s*(.+)/);
        const biographyMatch = block.match(/Biography:\s*(.+)/s);

        return {
          name: nameMatch ? nameMatch[1].trim() : "",
          biography: biographyMatch ? biographyMatch[1].trim() : "",
        };
      })
      .filter((character) => character.name && character.biography);

    console.log("Parsed characters:", parsedCharacters); // Debug log
    return parsedCharacters;
  };

  const handleGenerateImages = async () => {
    setIsGeneratingImages(true);
    setShowImageModal(true);
    const newCharacterImages = {};

    for (const character of characters) {
      try {
        const response = await fetch("http://localhost:8000/generate-image/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: character.name,
            biography: character.biography,
            genre: genre,
          }),
        });
        const data = await response.json();
        newCharacterImages[character.name] = data.image_url;
      } catch (error) {
        console.error(`Error generating image for ${character.name}:`, error);
      }
    }

    setCharacterImages(newCharacterImages);
    setIsGeneratingImages(false);
  };

  const handleSendMessage = () => {
    const outgoingMessage = {
      direction: "outgoing",
      message: inputMessage,
      position: "single",
      sender: "You",
      sentTime: new Date().toLocaleTimeString(),
    };

    setData([...data, outgoingMessage]);
    setInputMessage("");
    setIsLoading(true);

    fetch("http://localhost:8000/test/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: outgoingMessage.message,
        genre: genre,
        temperature: temperature,
        model: model,
      }),
    })
      .then((res) => res.json())
      .then((response) => {
        console.log("API Response:", response.data); // Debug log

        const incomingMessage = {
          direction: "incoming",
          message: `Characters:\n${response.data.characters}\n\nPlot:\n${response.data.plot}\n\nScenes:\n${response.data.scenes}`,
          position: "single",
          sender: "Assistant",
          sentTime: new Date().toLocaleTimeString(),
        };

        console.log("Incoming message:", incomingMessage.message); // Debug log

        setData((prevData) => [...prevData, incomingMessage]);
        const parsedChars = parseCharacters(incomingMessage.message);
        setCharacters(parsedChars);
        setIsLoading(false);
      });
  };

  //   const handlePdfUpload = async (event) => {
  //     const file = event.target.files[0];
  //     if (file) {
  //       const formData = new FormData();
  //       formData.append("file", file);

  //       try {
  //         const response = await fetch("/api/upload-pdf", {
  //           method: "POST",
  //           body: formData,
  //         });

  //         if (!response.ok) {
  //           throw new Error("Network response was not ok");
  //         }

  //         const data = await response.json();
  //         console.log("File uploaded successfully", data);
  //         const incomingMessage = {
  //           direction: "incoming",
  //           message: `Characters:\n${data.characters}\n\nPlot:\n${response.data.plot}\n\nScenes:\n${response.data.scenes}`,
  //           position: "single",
  //           sender: "Assistant",
  //           sentTime: new Date().toLocaleTimeString(),
  //         };
  //         setData((prevData) => [...prevData, incomingMessage]);
  //       } catch (error) {
  //         console.error("Error uploading file", error);
  //       }
  //     }
  //   };

  return (
    <div className="flex justify-center gap-4">
      {/* <Gitgraph>
        {(gitgraph) => {
          // Create the main branch
          const main = gitgraph.branch("main");

          // Commit to the main branch
          main.commit("Games Started");
          main.commit("James joined the team");
          main.commit("James met with Elsa and Alice");

          const aliceBranch = main.branch("alice-branch");

          // Commit where James meets Elsa on the elsa-branch
          main.commit("James felt in love Elsa");

          // Commit where James meets Alice on the alice-branch
          aliceBranch.commit("James felt in love Alice");
        }}
      </Gitgraph> */}
      <div>
        <header>
          <p>Chat Interface</p>
        </header>
        <ChatContainer style={{ height: "500px", width: "800px" }}>
          <MessageList
            typingIndicator={
              isLoading ? (
                <TypingIndicator content="Response is generating" />
              ) : null
            }
          >
            {data.map((msg, index) => (
              <Message
                key={index}
                model={{
                  direction: msg.direction,
                  message: msg.message,
                  position: msg.position,
                  sender: msg.sender,
                  sentTime: msg.sentTime,
                }}
                className={msg.direction === "incoming" ? "text-left" : ""}
              >
                {msg.direction === "incoming" && (
                  <Avatar
                    name={msg.sender}
                    src="https://chatscope.io/storybook/react/assets/emily-xzL8sDL2.svg"
                  />
                )}
              </Message>
            ))}
          </MessageList>
        </ChatContainer>

        {/* Modified button code */}
        {characters && characters.length > 0 ? (
          <Button
            variant="primary"
            onClick={handleGenerateImages}
            className="mt-3 mb-3"
            disabled={isGeneratingImages}
          >
            {isGeneratingImages
              ? "Generating Images..."
              : "Generate Character Images"}
          </Button>
        ) : (
          <div style={{ display: "none" }}>No characters available</div>
        )}

        <Form.Select
          aria-label="Select genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        >
          <option value="Fantasy">Fantasy</option>
          <option value="Action">Action</option>
          <option value="Horror">Horror</option>
          <option value="Humor">Humor</option>
          <option value="SciFi">SciFi</option>
          <option value="Romantic">Romantic</option>
        </Form.Select>
        <Form.Label>
          Creativity (Temperature): {temperature.toFixed(1)}
        </Form.Label>
        <FormRange
          min={0.0}
          max={1.0}
          step={0.1}
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
        />
        <Form>
          {["radio"].map((type) => (
            <div key={`inline-${type}`} className="mb-3">
              <Form.Check
                inline
                label="gpt-3.5-turbo"
                name="group1"
                type={type}
                id={`inline-${type}-1`}
                checked={model === "gpt-3.5-turbo"}
                onChange={() => setModel("gpt-3.5-turbo")}
              />
              <Form.Check
                inline
                label="gpt4"
                name="group1"
                type={type}
                id={`inline-${type}-2`}
                checked={model === "gpt4"}
                onChange={() => setModel("gpt4")}
              />
              {/* <Form.Check
              inline
              label="mistral-ai"
              name="group1"
              type={type}
              id={`inline-${type}-3`}
              checked={model === "mistral-ai"}
              onChange={() => setModel("mistral-ai")}
            /> */}
            </div>
          ))}
        </Form>
        <Modal
          show={showImageModal}
          onHide={() => setShowImageModal(false)}
          size="lg"
          centered
        >
          <Modal.Header closeButton>
            <Modal.Title>Character Images</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {isGeneratingImages ? (
              <div className="text-center">
                <p>Generating character images...</p>
                {/* You could add a spinner here */}
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(characterImages).map(([name, imageUrl]) => (
                  <div key={name} className="text-center">
                    <h4>{name}</h4>
                    <img
                      src={imageUrl}
                      alt={name}
                      className="max-w-full h-auto rounded"
                    />
                  </div>
                ))}
              </div>
            )}
          </Modal.Body>
        </Modal>
        <InputGroup className="mb-3">
          <Form.Control
            placeholder="Type your message here"
            aria-label="Message"
            aria-describedby="button-addon2"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />
          <Button
            variant="outline-secondary"
            id="button-addon2"
            onClick={handleSendMessage}
          >
            Send
          </Button>
        </InputGroup>
        {/* <InputGroup className="mb-3">
          <Form.Control
            type="file"
            accept="application/pdf"
            onChange={handlePdfUpload}
          />
        </InputGroup> */}
      </div>
    </div>
  );
}

export default App;
