<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Algoritmo <small> Apriori</small>
    </h1>
    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-row>
          <b-form-file ref="file" v-model="file" />
          <b-form-input
            v-model="confianza"
            type="number"
            :step="0.01"
            placeholder="Confianza"
          />
          <b-form-input
            v-model="soporte"
            type="number"
            :step="0.01"
            placeholder="Soporte"
          />
          <b-form-input
            v-model="elevacion"
            type="number"
            :step="0.01"
            placeholder="Elevación"
          />
        </b-row>
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

    <b-row>
      <b-col cols="12">
        <b-table striped hover :items="transactions" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
      <b-col cols="12">
        <b-img v-if="graphImg" :src="graphImg" fluid />
      </b-col>
    </b-row>

    <iframe
      src="http://localhost:5000/static/documentos/generados/apriori.pdf"
      width="600"
      height="780"
      style="border: none"
    ></iframe>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader',
  data() {
    return {
      file: null,
      soporte: null,
      confianza: null,
      elevacion: null,
      data: [],
      transactions: [],
      loading: false,
      error: null,
      graphImg: null,
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null
      this.graphImg = null
      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('soporte', this.soporte)
        formData.append('confianza', this.confianza)
        formData.append('elevacion', this.elevacion)
        const response = await this.$axios.$post(
          '/algoritmoApriori',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )

        this.data = JSON.parse(response.data)
        this.transactions = JSON.parse(response.transactions)
        this.graphImg = this.$axios.defaults.baseURL + '/' + response.graph
      } catch (error) {
        this.error = error.response.data.message
      } finally {
        this.loading = false
      }
    },
    clearData() {
      this.data = []
      this.transactions = []
      this.graphImg = null
      this.file = null
    },
  },
}
</script>

<style></style>
