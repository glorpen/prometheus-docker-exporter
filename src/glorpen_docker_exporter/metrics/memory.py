from prometheus_client import Counter, Gauge

from glorpen_docker_exporter.metrics import Stat


@Stat
def container_mem_usage_bytes(metric: Gauge, data: dict):
    """Current memory usage"""
    metric.set(data["memory_stats"]["usage"])


@Stat
def container_mem_max_usage_bytes(metric: Counter, data: dict):
    """Container max memory usage recorded"""
    metric.inc(data["memory_stats"]["max_usage"])


@Stat
def container_mem_usage_limit_bytes(metric: Gauge, data: dict):
    """Container current memory usage limit"""
    metric.inc(data["memory_stats"]["limit"])


@Stat
def container_mem_active_anon_bytes(metric: Gauge, data: dict):
    """Anonymous and swap cache memory on active LRU list"""
    metric.set(data["memory_stats"]["stats"]["active_anon"])


@Stat
def container_mem_active_file_bytes(metric: Gauge, data: dict):
    """File-backed memory on active LRU list"""
    metric.set(data["memory_stats"]["stats"]["active_file"])


@Stat
def container_mem_cache_bytes(metric: Gauge, data: dict):
    """Page cache memory"""
    metric.set(data["memory_stats"]["stats"]["cache"])


@Stat
def container_mem_dirty_bytes(metric: Gauge, data: dict):
    """Bytes that are waiting to get written back to the disk."""
    metric.set(data["memory_stats"]["stats"]["dirty"])


@Stat
def container_mem_hierarchical_memory_limit_bytes(metric: Gauge, data: dict):
    """Memory limit with regard to hierarchy under which the memory cgroup is"""
    metric.set(data["memory_stats"]["stats"]["hierarchical_memory_limit"])


@Stat
def container_mem_hierarchical_memsw_limit_bytes(metric: Gauge, data: dict):
    """Memory+swap limit with regard to hierarchy under which memory cgroup is"""
    metric.set(data["memory_stats"]["stats"]["hierarchical_memsw_limit"])


@Stat
def container_mem_inactive_anon_bytes(metric: Gauge, data: dict):
    """Anonymous and swap cache memory on inactive LRU list"""
    metric.set(data["memory_stats"]["stats"]["inactive_anon"])


@Stat
def container_mem_inactive_file_bytes(metric: Gauge, data: dict):
    """File-backed memory on inactive LRU list"""
    metric.set(data["memory_stats"]["stats"]["inactive_file"])


@Stat
def container_mem_mapped_file_bytes(metric: Gauge, data: dict):
    """Size of mapped files (includes tmpfs/shmem)"""
    metric.set(data["memory_stats"]["stats"]["mapped_file"])


@Stat
def container_mem_pgfault_count(metric: Counter, data: dict):
    """Count of reported page faults"""
    metric.inc(data["memory_stats"]["stats"]["pgfault"])


@Stat
def container_mem_pgmajfault_count(metric: Counter, data: dict):
    """Count of reported major page faults"""
    metric.inc(data["memory_stats"]["stats"]["pgmajfault"])


@Stat
def container_mem_pgpgin_count(metric: Counter, data: dict):
    """
    Count of charging events to the memory cgroup. The charging
    event happens each time a page is accounted as either mapped
    anon page(RSS) or cache page(Page Cache) to the cgroup.
    """
    metric.inc(data["memory_stats"]["stats"]["pgpgin"])


@Stat
def container_mem_pgpgout_count(metric: Counter, data: dict):
    """
    Count uncharging events to the memory cgroup. The uncharging
    event happens each time a page is unaccounted from the cgroup.
    """
    metric.inc(data["memory_stats"]["stats"]["pgpgout"])


@Stat
def container_mem_rss_bytes(metric: Gauge, data: dict):
    """Bytes of anonymous and swap cache memory (includes transparent hugepages)."""
    metric.inc(data["memory_stats"]["stats"]["rss"])


@Stat
def container_mem_rss_huge_bytes(metric: Gauge, data: dict):
    """Bytes of anonymous transparent hugepages."""
    metric.inc(data["memory_stats"]["stats"]["rss_huge"])


@Stat
def container_mem_writeback_bytes(metric: Gauge, data: dict):
    """Bytes of file/anon cache that are queued for syncing to disk."""
    metric.inc(data["memory_stats"]["stats"]["writeback"])


@Stat
def container_mem_unevictable_bytes(metric: Gauge, data: dict):
    """Bytes of memory that cannot be reclaimed (mlocked etc)."""
    metric.inc(data["memory_stats"]["stats"]["unevictable"])


@Stat
def container_mem_hierarchical_active_anon_bytes(metric: Gauge, data: dict):
    """Sum of anonymous and swap cache memory on active LRU list in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_active_anon"])


@Stat
def container_mem_hierarchical_active_file_bytes(metric: Gauge, data: dict):
    """Sum of file-backed memory on active LRU list in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_active_file"])


@Stat
def container_mem_hierarchical_cache_bytes(metric: Gauge, data: dict):
    """Sum of page cache memory in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_cache"])


@Stat
def container_mem_hierarchical_dirty_bytes(metric: Gauge, data: dict):
    """Bytes that are waiting to get written back to the disk in cgroup branch."""
    metric.set(data["memory_stats"]["stats"]["total_dirty"])


@Stat
def container_mem_hierarchical_inactive_anon_bytes(metric: Gauge, data: dict):
    """Sum of anonymous and swap cache memory on inactive LRU list in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_inactive_anon"])


@Stat
def container_mem_hierarchical_inactive_file_bytes(metric: Gauge, data: dict):
    """Sum of file-backed memory on inactive LRU list in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_inactive_file"])


@Stat
def container_mem_hierarchical_mapped_file_bytes(metric: Gauge, data: dict):
    """Size of mapped files (includes tmpfs/shmem) in cgroup branch"""
    metric.set(data["memory_stats"]["stats"]["total_mapped_file"])


@Stat
def container_mem_hierarchical_pgfault_count(metric: Counter, data: dict):
    """Count of reported page faults in cgroup branch"""
    metric.inc(data["memory_stats"]["stats"]["total_pgfault"])


@Stat
def container_mem_hierarchical_pgmajfault_count(metric: Counter, data: dict):
    """Count of reported major page faults in cgroup branch"""
    metric.inc(data["memory_stats"]["stats"]["total_pgmajfault"])


@Stat
def container_mem_hierarchical_pgpgin_count(metric: Counter, data: dict):
    """
    Count of charging events to the memory cgroup branch. The charging
    event happens each time a page is accounted as either mapped
    anon page(RSS) or cache page(Page Cache) to the cgroup.
    """
    metric.inc(data["memory_stats"]["stats"]["total_pgpgin"])


@Stat
def container_mem_hierarchical_pgpgout_count(metric: Counter, data: dict):
    """
    Count uncharging events to the memory cgroup branch. The uncharging
    event happens each time a page is unaccounted from the cgroup.
    """
    metric.inc(data["memory_stats"]["stats"]["total_pgpgout"])


@Stat
def container_mem_hierarchical_rss_bytes(metric: Gauge, data: dict):
    """Bytes of anonymous and swap cache memory in cgroup branch (includes transparent hugepages)."""
    metric.inc(data["memory_stats"]["stats"]["total_rss"])


@Stat
def container_mem_hierarchical_rss_huge_bytes(metric: Gauge, data: dict):
    """Bytes of anonymous transparent hugepages in cgroup branch."""
    metric.inc(data["memory_stats"]["stats"]["total_rss_huge"])


@Stat
def container_mem_hierarchical_writeback_bytes(metric: Gauge, data: dict):
    """Bytes of file/anon cache that are queued for syncing to disk in cgroup branch."""
    metric.inc(data["memory_stats"]["stats"]["total_writeback"])


@Stat
def container_mem_hierarchical_unevictable_bytes(metric: Gauge, data: dict):
    """Bytes of memory that cannot be reclaimed in cgroup branch (mlocked etc)."""
    metric.inc(data["memory_stats"]["stats"]["total_unevictable"])
