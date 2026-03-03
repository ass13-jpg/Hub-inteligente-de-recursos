import React, { useState, useEffect, useCallback } from 'react';
import { Edit2, Trash2, Plus } from 'lucide-react';
import { resourcesAPI } from '../services/api';

export default function ResourceList({ onEdit, onNew, refresh }) {
  // Inicializamos garantindo que é um array vazio
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ skip: 0, limit: 10, total: 0 });

  const loadResources = useCallback(async () => {
    setLoading(true);
    try {
      const response = await resourcesAPI.list(pagination.skip, pagination.limit);
      
      // 🛡️ A CORREÇÃO DE OURO: 
      // Lê o array diretamente se o backend mandar assim, ou procura em "items"
      const dataItems = Array.isArray(response.data) ? response.data : (response.data?.items || []);
      const dataTotal = response.data?.total !== undefined ? response.data.total : dataItems.length;

      setResources(dataItems);
      setPagination((prev) => ({
        ...prev,
        total: dataTotal,
      }));
    } catch (err) {
      console.error('Erro ao carregar recursos:', err);
      // Garantimos que não fique undefined caso a requisição falhe
      setResources([]); 
    } finally {
      setLoading(false);
    }
  }, [pagination.skip, pagination.limit]);

  useEffect(() => {
    loadResources();
  }, [loadResources, refresh]);

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja deletar este recurso?')) {
      try {
        await resourcesAPI.delete(id);
        if (resources.length === 1 && pagination.skip > 0) {
          setPagination(prev => ({ ...prev, skip: prev.skip - prev.limit }));
        } else {
          loadResources();
        }
      } catch (err) {
        console.error('Erro ao deletar:', err);
      }
    }
  };

  const goToNextPage = () => {
    setPagination((prev) => ({ ...prev, skip: prev.skip + prev.limit }));
  };

  const goToPreviousPage = () => {
    setPagination((prev) => ({ ...prev, skip: Math.max(0, prev.skip - prev.limit) }));
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Recursos Educacionais</h2>
        <button
          onClick={onNew}
          className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Novo Recurso
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-6 py-3 text-left font-semibold">Título</th>
              <th className="px-6 py-3 text-left font-semibold">Tipo</th>
              <th className="px-6 py-3 text-left font-semibold">Tags</th>
              <th className="px-6 py-3 text-center font-semibold">Ações</th>
            </tr>
          </thead>
          
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="4" className="text-center py-8 text-gray-500">
                  <div className="flex justify-center items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-500"></div>
                    Carregando...
                  </div>
                </td>
              </tr>
            ) : resources.length === 0 ? (
              <tr>
                <td colSpan="4" className="text-center py-8 text-gray-500">
                  Nenhum recurso cadastrado
                </td>
              </tr>
            ) : (
              resources.map((resource) => (
                <tr key={resource.id} className="border-t hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium">{resource.title}</td>
                  <td className="px-6 py-4">
                    <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded">
                      {resource.resource_type}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {/* Renderização protegida das tags */}
                    {resource.tags && (Array.isArray(resource.tags) ? resource.tags : String(resource.tags).split(','))
                      .map((tag, index) => {
                        const cleanTag = tag.trim();
                        if (!cleanTag) return null;
                        return (
                          <span
                            key={`${cleanTag}-${index}`}
                            className="inline-block bg-gray-200 text-gray-800 px-2 py-1 rounded mr-1 text-xs mb-1"
                          >
                            {cleanTag}
                          </span>
                        );
                      })}
                  </td>
                  <td className="px-6 py-4 text-center flex justify-center gap-2">
                    <button
                      onClick={() => onEdit(resource)}
                      className="text-blue-600 hover:text-blue-800 p-2"
                      title="Editar"
                    >
                      <Edit2 className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(resource.id)}
                      className="text-red-600 hover:text-red-800 p-2"
                      title="Deletar"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {!loading && resources.length > 0 && (
        <div className="flex justify-between items-center mt-6">
          <div className="text-sm text-gray-600">
            Mostrando {pagination.skip + 1} a{' '}
            {Math.min(pagination.skip + pagination.limit, pagination.total)} de{' '}
            {pagination.total} recursos
          </div>
          <div className="flex gap-2">
            <button
              onClick={goToPreviousPage}
              disabled={pagination.skip === 0}
              className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 hover:bg-gray-50 transition-colors"
            >
              Anterior
            </button>
            <button
              onClick={goToNextPage}
              disabled={pagination.skip + pagination.limit >= pagination.total}
              className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 hover:bg-gray-50 transition-colors"
            >
              Próxima
            </button>
          </div>
        </div>
      )}
    </div>
  );
}