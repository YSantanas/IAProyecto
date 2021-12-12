<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Algoritmo <small> Regresión Lineal</small>
    </h1>
    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-form-file ref="file" v-model="file" />
        <p class="p-3 mb-2 bg-dark text-white">Datos para nuevos pronosticos</p>
        <b-form-input
          v-model="profundidad1"
          type="number"
          placeholder="profundidad"
        />
        <b-form-input v-model="r1" type="number" placeholder="r1" />
        <b-form-input v-model="r2" type="number" placeholder="r2" />
        <b-form-input v-model="r3" type="number" placeholder="r3" />
        <b-row align-v="center">
          <b-button
            :disabled="!file"
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
            :disabled="!file"
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

    <b-col cols="9">
      <b-table striped hover :items="data" :busy="loading" responsive>
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-col>

    <b-col cols="9">
      <b-table striped hover :items="data2" :busy="loading" responsive>
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-col>

    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg" :src="graphImg" fluid />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg2" :src="graphImg2" fluid />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg3" :src="graphImg3" fluid />
      </b-col>
    </b-row>

    <b-row v-if="graphImg">
      <b-col cols="12">
        <b-alert variant="success" :show="resultado != null"
          ><span class="font-weight-bold">Resultado del nuevo pronostico:</span
          >{{ resultado }}</b-alert
        >
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader5',
  data() {
    return {
      file: null,
      data: [],
      data2: [],
      resultado: [],
      loading: false,
      error: null,
      graphImg: null,
      graphImg2: null,
      graphImg3: null,
      profundidad1: null,
      r1: null,
      r2: null,
      r3: null,
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('profundidad1', this.profundidad1)
        formData.append('r1', this.r1)
        formData.append('r2', this.r2)
        formData.append('r3', this.r3)

        const response = await this.$axios.$post('/regresionLineal', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        this.data = JSON.parse(response.data)
        this.data2 = JSON.parse(response.data2)
        this.resultado = JSON.parse(response.newpronostico)

        this.graphImg = this.$axios.defaults.baseURL + '/' + response.graph
        this.graphImg2 = this.$axios.defaults.baseURL + '/' + response.graph2
        this.graphImg3 = this.$axios.defaults.baseURL + '/' + response.graph3
      } catch (error) {
        this.error = error.response.data.message
      } finally {
        this.loading = false
      }
    },
    clearData() {
      this.data = []
      this.data2 = []
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.file = null
      this.resultado = null
      this.profundidad1 = null
      this.r1 = null
      this.r2 = null
      this.r3 = null
    },
  },
}
</script>

<style></style>
