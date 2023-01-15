#include "stdafx.h"

void ShowForwardReverseTimeForTuning(const PNGraph& Graph) {
  int pairCount = 10000;
  TRnd Rnd(42); // keep same seed for reproduceability
  TTmStopWatch w;
  w.Start();
  for (int i = 0; i < pairCount; i++) {
    int startId = Graph->GetRndNId();
    int targetId = Graph->GetRndNId();
    printf("PPR from node %d to node %d: %g\n", startId, targetId,
           TSnap::GetPersonalizedPageRankBidirectional(Graph, 0.2, TIntV::GetV(startId), targetId, 0.1f, 4.0f / Graph->GetNodes(), false, true));
  }
  printf("Total time for %d pairs: %g\n", pairCount, w.GetSec());
}

int main(int argc, char* argv[]) {
  Env = TEnv(argc, argv, TNotify::StdNotify);
  Env.PrepArgs(TStr::Fmt("Pagerank build: %s, %s. Time: %s", __TIME__, __DATE__, TExeTm::GetCurTm()));
  Try
  const TStr InFNm = Env.GetIfArgPrefixStr("-i:", "../graphs/twitter_combined.txt", "Input un/directed graph");
  PNGraph Graph = TSnap::LoadEdgeList<PNGraph>(InFNm, 0, 1, ',');
  
  ShowForwardReverseTimeForTuning(Graph);
  
  Catch
  return 0;
}
