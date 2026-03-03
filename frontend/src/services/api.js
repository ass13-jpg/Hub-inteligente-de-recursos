import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const resourcesAPI = {
  list: (skip = 0, limit = 10) =>
    api.get('/resources', { params: { skip, limit } }),
  create: (data) => api.post('/resources', data),
  get: (id) => api.get(`/resources/${id}`),
  update: (id, data) => api.put(`/resources/${id}`, data),
  delete: (id) => api.delete(`/resources/${id}`),
};

export const aiAPI = {
  assist: (title, resourceType) =>
    api.post('/ai/assist', { title, resource_type: resourceType }),
};

export default api;