<template>
  <div class="container">
    <h1>Operadoras</h1>
    <input v-model="query" @input="buscarOperadoras" placeholder="Buscar por nome fantasia" class="search-input" />
    
    <div class="table-responsive">
      <table v-if="paginatedOperadoras.length">
        <thead>
          <tr>
            <th v-for="(header, index) in headers" :key="index">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operadora in paginatedOperadoras" :key="operadora.Registro_ANS">
            <td>{{ operadora.Registro_ANS }}</td>
            <td>{{ operadora.CNPJ }}</td>
            <td>{{ operadora.Razao_Social }}</td>
            <td>{{ operadora.Nome_Fantasia }}</td>
            <td>{{ operadora.Modalidade }}</td>
            <td>{{ operadora.Logradouro }}</td>
            <td>{{ operadora.Numero }}</td>
            <td>{{ operadora.Complemento }}</td>
            <td>{{ operadora.Bairro }}</td>
            <td>{{ operadora.Cidade }}</td>
            <td>{{ operadora.UF }}</td>
            <td>{{ operadora.CEP }}</td>
            <td>{{ operadora.DDD }}</td>
            <td>{{ operadora.Telefone }}</td>
            <td>{{ operadora.Fax }}</td>
            <td>{{ operadora.Endereco_eletronico }}</td>
            <td>{{ operadora.Representante }}</td>
            <td>{{ operadora.Cargo_Representante }}</td>
            <td>{{ operadora.Regiao_de_Comercializacao }}</td>
            <td>{{ operadora.Data_Registro_ANS }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>Sem resultados para a busca...</p>
    </div>

    <!-- Paginação -->
    <div class="pagination" v-if="operadoras.length > itemsPerPage">
      <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
      <span>Página {{ currentPage }} de {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      operadoras: [],
      currentPage: 1,
      itemsPerPage: 10, // Número de itens por página
      headers: [
        'Registro ANS', 'CNPJ', 'Razão Social', 'Nome Fantasia', 'Modalidade',
        'Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade', 'UF', 'CEP',
        'DDD', 'Telefone', 'Fax', 'Endereço Eletrônico', 'Representante',
        'Cargo', 'Região', 'Data de Registro ANS'
      ]
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.operadoras.length / this.itemsPerPage);
    },
    paginatedOperadoras() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.operadoras.slice(start, end);
    }
  },
  methods: {
    async buscarOperadoras() {
      try {
        console.log(`URL chamada: https://intuitivecareextra.onrender.com/buscar-operadoras?query=${this.query}`);
        const response = await axios.get(`https://intuitivecareextra.onrender.com/buscar-operadoras?query=${this.query}`);
        this.operadoras = response.data;
        this.currentPage = 1; // Resetar para a primeira página
      } catch (error) {
        console.error('Erro ao buscar operadoras:', error);
      }
    },
     nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
     },
     prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    }
  },
  created() {
    this.buscarOperadoras(); // Carregar todas as operadoras inicialmente
  },
};
</script>

<style scoped>
.container {
  padding: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1.5rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #8e44ad;
  outline: none;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

table {
  width: auto;
  min-width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

th, td {
  padding: 0.6rem 0.8rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  white-space: nowrap;
}

th {
  background-color: #8e44ad; /* Roxo */
  color: white;
  font-size: 1rem;
  font-weight: 600;
  position: sticky;
  top: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
td {
  white-space: nowrap;
  vertical-align: middle;
}
/* Barra de rolagem - garantindo que apareça */
.table-responsive {
  overflow-x: scroll;
  scrollbar-width: thin; /* Para Firefox */
}

.table-responsive::-webkit-scrollbar {
  height: 8px; /* Mais visível */
}

.table-responsive::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.table-responsive::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.table-responsive::-webkit-scrollbar-thumb:hover {
  background: #555;
}
p {
  padding: 1.5rem;
  text-align: center;
  color: #666;
  font-size: 1rem;
}
</style>