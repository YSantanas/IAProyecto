<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Algoritmo <small> Cluster Particional</small>
    </h1>
    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-row>
          <b-form-file ref="file" v-model="file" />
          <b-form-input
            v-model="variableEvalP"
            type="text"
            placeholder="variable de Eval"
          />

          <b-form-input
            v-model="numClusterP"
            type="number"
            placeholder="Numero de cluster Particional"
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
      <b-table
        v-if="data"
        striped
        hover
        :items="data"
        :busy="loading"
        responsive
      >
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-col>

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
        <b-img v-if="graphImg" :src="graphImg" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg" :src="graphImg2" fluid />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg" :src="graphImg3" fluid />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader4',
  data() {
    return {
      file: null,
      data: [],
      loading: false,
      error: null,
      graphImg: null,
      graphImg2: null,
      graphImg3: null,
      variableEvalP: null,
      numClusterP: null,
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null
      this.graphImg = null
      this.graphImg2 = null
      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('variableEvalP', this.variableEvalP)
        formData.append('numClusterP', this.numClusterP)

        const response = await this.$axios.$post(
          '/clusterParticional',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )

        this.data = JSON.parse(response.data)

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
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.file = null
    },
  },
}
</script>

<style></style>
