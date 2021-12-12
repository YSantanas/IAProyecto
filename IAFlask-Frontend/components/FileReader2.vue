<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Algoritmo <small> Metricas Distancia</small>
    </h1>
    <b-row align-h="center">
      <b-col cols="3" class="my-4">
        <b-row style="row-gap: 0.5rem">
          <b-form-file ref="file" v-model="file" required />
          <b-form-input
            v-model="input_a"
            required
            type="number"
            step="1"
            min="0"
            placeholder="Item A"
          />
          <b-form-input
            v-model="input_b"
            required
            type="number"
            step="1"
            min="0"
            placeholder="Item B"
          />
        </b-row>
        <b-row align-v="center">
          <b-button
            :disabled="!file || !input_a || !input_b"
            class="mt-2"
            variant="primary"
            block
            @click="readFile"
          >
            Upload
          </b-button>
          <div v-if="error" class="text-danger small ml-2">
            {{ error }}
          </div>
        </b-row>
        <b-row>
          <b-button
            :disabled="!file || !input_a || !input_b"
            class="mt-2"
            variant="danger"
            block
            @click="clearData"
          >
            Clear
          </b-button>
        </b-row>
      </b-col>
    </b-row>
    <b-table striped hover :items="data" :busy="loading" responsive>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-table striped hover :items="dataChebyshev" :busy="loading" responsive>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-alert class="w-100" :show="dataChebyshev.length > 0">
      <span class="font-weight-bold">Distancia Chebyshev:</span> {{ distChebyshev }}
    </b-alert>
    <b-table striped hover :items="dataEuclidiana" :busy="loading" responsive>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-alert class="w-100" :show="dataEuclidiana.length > 0">
      <span class="font-weight-bold">Distancia Euclidiana:</span> {{ distEuclidiana }}
    </b-alert>
    <b-table striped hover :items="dataManhattan" :busy="loading" responsive>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-alert class="w-100" :show="dataManhattan.length > 0">
      <span class="font-weight-bold">Distancia Manhattan:</span> {{ distManhattan }}
    </b-alert>
    <b-table striped hover :items="dataMinkowski" :busy="loading" responsive>
      <template #table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-alert class="w-100" :show="dataMinkowski.length > 0">
      <span class="font-weight-bold">Distancia Minkowski:</span> {{ distMinkowski }}
    </b-alert>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader4',
  data() {
    return {
      data: [],
      dataChebyshev: [],
      dataEuclidiana: [],
      dataManhattan: [],
      dataMinkowski: [],
      distChebyshev: null,
      distEuclidiana: null,
      distManhattan: null,
      distMinkowski: null,
      error: null,
      file: null,
      input_a: null,
      input_b: null,
      loading: false,
      transactions: [],
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null

      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('input_a', this.input_a)
        formData.append('input_b', this.input_b)
        const response = await this.$axios.$post(
          '/medidasDistancias',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )
        this.data = JSON.parse(response.data)
        this.dataChebyshev = JSON.parse(response.data_chebyshev)
        this.dataEuclidiana = JSON.parse(response.data_euclidiana)
        this.dataManhattan = JSON.parse(response.data_manhattan)
        this.dataMinkowski = JSON.parse(response.data_minkowski)
        this.distChebyshev = response.dist_chebyshev
        this.distEuclidiana = response.dist_euclidiana
        this.distManhattan = response.dist_manhattan
        this.distMinkowski = response.dist_minkowski
      } catch (error) {
        this.error = error.response.data.message
      } finally {
        this.loading = false
      }
    },
    clearData() {
      this.data = []
      this.transactions = []
      this.file = null
    },
  },
}
</script>

<style></style>
