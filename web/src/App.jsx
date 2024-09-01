import "./App.css";
import { useState, useEffect } from "react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import "./index.css";
import "bootstrap/dist/css/bootstrap.css";
import { Gitgraph } from "@gitgraph/react";

import {
  ChatContainer,
  MessageList,
  Message,
  Avatar,
} from "@chatscope/chat-ui-kit-react";

import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import FormRange from "react-bootstrap/FormRange";

function App() {
  const [data, setData] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [genre, setGenre] = useState("Fantasy");
  const [temperature, setTemperature] = useState(0.0);
  const [model, setModel] = useState("gpt-3.5-turbo");

  useEffect(() => {
    // Fetch initial data or previous messages if needed
  }, []);

  const handleSendMessage = () => {
    fetch("http://localhost:8000/test/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: inputMessage,
        genre: genre,
        temperature: temperature,
        model: model,
      }), // Send the genre
    })
      .then((res) => res.json())
      .then((response) => {
        console.log(response); // Log the response to inspect its structure
        setData([
          ...data,
          {
            direction: "outgoing",
            message: inputMessage,
            position: "single",
            sender: "You",
            sentTime: new Date().toLocaleTimeString(),
          },
          {
            direction: "incoming",
            message: `Characters:\n${response.data.characters}\n\nPlot:\n${response.data.plot}\n\nScenes:\n${response.data.scenes}`,
            position: "single",
            sender: "Assistant",
            sentTime: new Date().toLocaleTimeString(),
          },
        ]);
        setInputMessage(""); // Clear the input field
      });
  };

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
        <ChatContainer
          style={{
            height: "500px",
            width: "800px",
          }}
        >
          <MessageList>
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
      </div>
    </div>
  );
}

export default App;
