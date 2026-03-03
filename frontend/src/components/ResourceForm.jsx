import React, { useState } from 'react';
import { Sparkles, Loader } from 'lucide-react';
import { aiAPI, resourcesAPI } from '../services/api';

export default function ResourceForm({ resource, onSubmit, onCancel }) {
  // Inicializamos o estado. Se vier tags do backend (em array), transformamos em string separada por vírgula.
  const [formData, setFormData] = useState({
    title: resource?.title || '',
    description: resource?.description || '',
    resource_type: resource?.resource_type || 'Video',
    url: resource?.url || '',
    tags: resource?.tags 
      ? (Array.isArray(resource.tags) ? resource.tags.join(', ') : String(resource.tags)) 
      : '',
  });

  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleAIAssist = async () => {
    if (!formData.title.trim()) {
      setError('Título é obrigatório para usar a IA');
      return;
    }

    setAiLoading(true);
    setError('');

    try {
      const response = await aiAPI.assist(formData.title, formData.resource_type);
      
      // A IA provavelmente retorna um array. Convertamos para string para colocar no input.
      const aiTags = response.data.tags;
      const formattedTags = Array.isArray(aiTags) ? aiTags.join(', ') : String(aiTags || '');

      setFormData((prev) => ({
        ...prev,
        description: response.data.description || prev.description,
        tags: formattedTags,
      }));
    } catch (err) {
      setError('Erro ao gerar conteúdo com IA. Tente novamente.');
      console.error(err);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // TRANSFORMA O TEXTO DE VOLTA EM ARRAY ANTES DE MANDAR PRO BACKEND
      // Divide por vírgula, remove espaços extras e ignora itens vazios
      const tagsArray = formData.tags
        ? formData.tags.split(',').map(tag => tag.trim()).filter(tag => tag !== '')
        : [];

      const dataToSubmit = {
        ...formData,
        tags: tagsArray
      };

      if (resource?.id) {
        await resourcesAPI.update(resource.id, dataToSubmit);
      } else {
        await resourcesAPI.create(dataToSubmit);
      }
      
      onSubmit(); // Fecha o form e recarrega a lista
    } catch (err) {
      // Captura segura de mensagens de erro do backend FastAPI
      setError(err.response?.data?.detail || err.message || 'Erro ao salvar recurso');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Tratamento para evitar crash caso "error" venha como objeto inesperado
  const renderError = () => {
    if (!error) return null;
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700">
        {typeof error === 'string' ? error : JSON.stringify(error)}
      </div>
    );
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md space-y-4">
      <h2 className="text-2xl font-bold text-gray-800">
        {resource ? 'Editar Recurso' : 'Novo Recurso'}
      </h2>

      {renderError()}

      <div>
        <label className="block text-sm font-medium text-gray-700">Título *</label>
        <input
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Ex: Introdução a Cálculo Diferencial"
          required
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Tipo *</label>
        <select
          name="resource_type"
          value={formData.resource_type}
          onChange={handleChange}
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        >
          <option value="Video">Video</option>
          <option value="PDF">PDF</option>
          <option value="Link">Link</option>
        </select>
      </div>

      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="block text-sm font-medium text-gray-700">Descrição</label>
          <button
            type="button"
            onClick={handleAIAssist}
            disabled={aiLoading}
            className="flex items-center gap-2 text-sm bg-gradient-to-r from-purple-500 to-pink-500 text-white px-3 py-1 rounded-lg hover:shadow-lg disabled:opacity-50 transition-all"
          >
            {aiLoading ? (
              <Loader className="w-4 h-4 animate-spin" />
            ) : (
              <Sparkles className="w-4 h-4" />
            )}
            {aiLoading ? 'Gerando...' : 'Gerar com IA'}
          </button>
        </div>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Descrição do recurso"
          rows="4"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">URL</label>
        <input
          type="url"
          name="url"
          value={formData.url}
          onChange={handleChange}
          placeholder="https://exemplo.com"
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Tags (separadas por vírgula)</label>
        <input
          type="text"
          name="tags"
          value={formData.tags}
          onChange={handleChange}
          placeholder="matemática, cálculo, educação"
          className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        />
      </div>

      <div className="flex gap-3 justify-end pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Salvando...' : 'Salvar'}
        </button>
      </div>
    </form>
  );
}