import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const askQuery = async (query) => {
  const response = await API.post("/ask", {
    query: query,
  });

  return response.data;
};

export const getSummary = async () => {
  const response = await API.get("/metrics/summary");
  return response.data;
};

export const getRequests = async () => {
  const response = await API.get("/metrics/requests");
  return response.data;
};

export default API;