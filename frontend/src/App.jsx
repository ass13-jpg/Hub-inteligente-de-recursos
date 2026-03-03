import React, { useState } from 'react';
import ResourceList from './components/ResourceList';
import ResourceForm from './components/ResourceForm';

function App() {
  const [view, setView] = useState('list');
  const [selectedResource, setSelectedResource] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleEdit = (resource) => {
    setSelectedResource(resource);
    setView('form');
  };

  const handleNew = () => {
    setSelectedResource(null);
    setView('form');
  };

  const handleFormSubmit = () => {
    setView('list');
    setRefreshKey((prev) => prev + 1);
  };

  const handleCancel = () => {
    setView('list');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-6 shadow-lg">
        <div className="max-w-7xl mx-auto px-6">
          <h1 className="text-3xl font-bold">🎓 Hub Inteligente de Recursos Educacionais</h1>
          <p className="text-blue-100 mt-2">Catalogação inteligente com IA</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {view === 'list' && (
          <ResourceList
            onEdit={handleEdit}
            onNew={handleNew}
            refresh={refreshKey}
          />
        )}

        {view === 'form' && (
          <ResourceForm
            resource={selectedResource}
            onSubmit={handleFormSubmit}
            onCancel={handleCancel}
          />
        )}
      </main>
    </div>
  );
}

export default App;